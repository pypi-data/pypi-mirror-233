"""
Copyright (C) 2021 Microsoft Corporation
"""
from typing import List, Dict
from collections import OrderedDict, defaultdict
import json
import xml.etree.ElementTree as ET
import os
from logging import WARNING
import matplotlib.backends.backend_agg as agg
import torch
from torchvision import transforms
from PIL import Image
from fitz import Rect
import numpy as np
import pandas as pd
from matplotlib import patches, pyplot as plt
from matplotlib.patches import Patch
from ..engine import postprocess
import onnxruntime
from easyocr import Reader
from tqdm import tqdm
import logging

class MaxResize():
    """
    MaxResize augmentation object.
    """
    def __init__(self, max_size=800):
        self.max_size = max_size

    def __call__(self, image):
        width, height = image.size
        current_max_size = max(width, height)
        scale = self.max_size / current_max_size
        resized_image = image.resize((int(round(scale*width)),
                                      int(round(scale*height))))
        return resized_image

structure_transform = transforms.Compose([
    MaxResize(1000),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


def get_class_map(data_type):
    """
    Get class map
    """
    if data_type == 'structure':
        class_map = {
            'table': 0,
            'table column': 1,
            'table row': 2,
            'table column header': 3,
            'table projected row header': 4,
            'table spanning cell': 5,
            'no object': 6
        }
    elif data_type == 'detection':
        class_map = {'table': 0, 'table rotated': 1, 'no object': 2}
    return class_map


def get_structure_class_thresholds(table: float = 0.5,
                                   table_column: float = 0.5,
                                   table_row: float = 0.5,
                                   table_column_header: float = 0.5,
                                   table_projected_row_header: float = 0.5,
                                   table_spanning_cell: float = 0.5,
                                   no_object: int = 10):
    """
    Get structure recognition threshold in dictionary format.

    Arguments:
        table: float, table structure recognition threshold = 0.5,
        table_column: float, table column recognition threshold = 0.5,
        table_row: float, table row recognition threshold = 0.5,
        table_column_header: float, table column header threshold = 0.5,
        table_projected_row_header: float, table projected row header
         threshold = 0.5,
        table_spanning_cell: float, table spanning cell recognition
         threshold = 0.5,
        no_object: int, number of objects = 10
    """
    return {
        'table': table,
        'table column': table_column,
        'table row': table_row,
        'table column header': table_column_header,
        'table projected row header': table_projected_row_header,
        'table spanning cell': table_spanning_cell,
        'no object': no_object
    }


# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    """
    Transform width height midpoint to 4 edges of box.
    """
    x_c, y_c, w, h = x.unbind(-1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h), (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)


def rescale_bboxes(out_bbox, size):
    """
    Rescale bounding box to the specified size.
    """
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b


def iob(bbox1, bbox2):
    """
    Compute the intersection area over box area, for bbox1.
    """
    intersection = Rect(bbox1).intersect(bbox2)
    bbox1_area = Rect(bbox1).get_area()
    if bbox1_area > 0:
        return intersection.get_area() / bbox1_area
    return 0


def align_headers(headers, rows):
    """
    Adjust the header boundary to be the convex hull of the rows it intersects
    at least 50% of the height of.

    For now, we are not supporting tables with multiple headers, so we need to
    eliminate anything besides the top-most header.
    """
    aligned_headers = []

    for row in rows:
        row['column header'] = False

    header_row_nums = []
    for header in headers:
        for row_num, row in enumerate(rows):
            row_height = row['bbox'][3] - row['bbox'][1]
            min_row_overlap = max(row['bbox'][1], header['bbox'][1])
            max_row_overlap = min(row['bbox'][3], header['bbox'][3])
            overlap_height = max_row_overlap - min_row_overlap
            if overlap_height / row_height >= 0.5:
                header_row_nums.append(row_num)

    if len(header_row_nums) == 0:
        return aligned_headers

    header_rect = Rect()
    if header_row_nums[0] > 0:
        header_row_nums = list(range(header_row_nums[0]+1)) + header_row_nums

    last_row_num = -1
    for row_num in header_row_nums:
        if row_num == last_row_num + 1:
            row = rows[row_num]
            row['column header'] = True
            header_rect = header_rect.include_rect(row['bbox'])
            last_row_num = row_num
        else:
            # Break as soon as a non-header row is encountered.
            # This ignores any subsequent rows in the table labeled as a \
            # header.
            # Having more than 1 header is not supported currently.
            break

    header = {'bbox': list(header_rect)}
    aligned_headers.append(header)

    return aligned_headers


def refine_table_structure(table_structure, class_thresholds):
    """
    Apply operations to the detected table structure objects such as
    thresholding, NMS, and alignment.
    """
    rows = table_structure["rows"]
    columns = table_structure['columns']

    # Process the headers
    column_headers = table_structure['column headers']
    column_headers = postprocess.apply_threshold(
        column_headers,
        class_thresholds["table column header"])
    column_headers = postprocess.nms(column_headers)
    column_headers = align_headers(column_headers, rows)

    # Process spanning cells
    spanning_cells = [elem for elem in table_structure['spanning cells']
                      if not elem['projected row header']]
    projected_row_headers = [elem for elem in table_structure['spanning cells']
                             if elem['projected row header']]
    spanning_cells = postprocess.apply_threshold(
        spanning_cells,
        class_thresholds["table spanning cell"])
    projected_row_headers = postprocess.apply_threshold(
        projected_row_headers,
        class_thresholds["table projected row header"])
    spanning_cells += projected_row_headers
    # Align before NMS for spanning cells because alignment brings \
    # them into agreement
    # with rows and columns first; if spanning cells still overlap \
    # after this operation,
    # the threshold for NMS can basically be lowered to just above 0
    spanning_cells = postprocess.align_supercells(spanning_cells, rows,
                                                  columns)
    spanning_cells = postprocess.nms_supercells(spanning_cells)

    postprocess.header_supercell_tree(spanning_cells)

    table_structure['columns'] = columns
    table_structure['rows'] = rows
    table_structure['spanning cells'] = spanning_cells
    table_structure['column headers'] = column_headers

    return table_structure


def outputs_to_objects(outputs, img_size, class_idx2name):
    """
    Transform model outputs to cell objects
    """
    m = outputs['pred_logits'].softmax(-1).max(-1)
    pred_labels = list(m.indices.detach().cpu().numpy())[0]
    pred_scores = list(m.values.detach().cpu().numpy())[0]
    pred_bboxes = outputs['pred_boxes'].detach().cpu()[0]
    pred_bboxes = [elem.tolist() for elem in rescale_bboxes(pred_bboxes,
                                                            img_size)]

    objects = []
    for label, score, bbox in zip(pred_labels, pred_scores, pred_bboxes):
        class_label = class_idx2name[int(label)]
        if not class_label == 'no object':
            objects.append({'label': class_label, 'score': float(score),
                            'bbox': [float(elem) for elem in bbox]})

    return objects




def objects_to_structures(objects, class_thresholds):
    """
    Process the bounding boxes produced by the \
        table structure recognition model into
    a *consistent* set of table structures \
        (rows, columns, spanning cells, headers).
    This entails resolving conflicts/overlaps, \
        and ensuring the boxes meet certain alignment
    conditions (for example: rows should all have the same width, etc.).
    """

    tables = [obj for obj in objects if obj['label'] == 'table']
    table_structures = []

    for table in tables:
        table_objects = [obj for obj in objects if iob(obj['bbox'],
                                                       table['bbox']) >= 0.5]
        structure = {}

        columns = [obj for obj in table_objects
                   if obj['label'] == 'table column']
        rows = [obj for obj in table_objects if obj['label'] == 'table row']
        column_headers = [obj for obj in table_objects
                          if obj['label'] == 'table column header']
        spanning_cells = [obj for obj in table_objects
                          if obj['label'] == 'table spanning cell']
        for obj in spanning_cells:
            obj['projected row header'] = False
        projected_row_headers = [
            obj for obj in table_objects
            if obj['label'] == 'table projected row header']
        for obj in projected_row_headers:
            obj['projected row header'] = True
        spanning_cells += projected_row_headers
        for obj in rows:
            obj['column header'] = False
            for header_obj in column_headers:
                if iob(obj['bbox'], header_obj['bbox']) >= 0.5:
                    obj['column header'] = True

        # Refine table structures
        rows = postprocess.refine_rows(rows,
                                       class_thresholds['table row'])
        columns = postprocess.refine_columns(columns,
                                             class_thresholds['table column'])
        # Shrink table bbox to just the total height of the rows
        # and the total width of the columns
        row_rect = Rect()
        for obj in rows:
            row_rect.include_rect(obj['bbox'])
        column_rect = Rect()
        for obj in columns:
            column_rect.include_rect(obj['bbox'])
        table['row_column_bbox'] = [column_rect[0], row_rect[1],
                                    column_rect[2], row_rect[3]]
        table['bbox'] = table['row_column_bbox']

        # Process the rows and columns into a complete segmented table
        columns = postprocess.align_columns(columns, table['row_column_bbox'])
        rows = postprocess.align_rows(rows, table['row_column_bbox'])

        structure['rows'] = rows
        structure['columns'] = columns
        structure['column headers'] = column_headers
        structure['spanning cells'] = spanning_cells

        if len(rows) > 0 and len(columns) > 1:
            structure = refine_table_structure(structure, class_thresholds)
        table_structures.append(structure)

    return table_structures


def structure_to_cells(table_structure):
    """
    Assuming the row, column, spanning cell, and header bounding boxes have
    been refined into a set of consistent table structures, process these
    table structures into table cells. This is a universal representation
    format for the table, which can later be exported to Pandas or CSV formats.
    Classify the cells as header/access cells or data cells
    based on if they intersect with the header bounding box.
    """
    columns = table_structure['columns']
    rows = table_structure['rows']
    spanning_cells = table_structure['spanning cells']
    cells = []
    subcells = []

    # Identify complete cells and subcells
    for column_num, column in enumerate(columns):
        for row_num, row in enumerate(rows):
            column_rect = Rect(list(column['bbox']))
            row_rect = Rect(list(row['bbox']))
            cell_rect = row_rect.intersect(column_rect)
            header = 'column header' in row and row['column header']
            cell = {'bbox': list(cell_rect),
                    'column_nums': [column_num],
                    'row_nums': [row_num],
                    'column header': header}

            cell['subcell'] = False
            for spanning_cell in spanning_cells:
                spanning_cell_rect = Rect(list(spanning_cell['bbox']))
                if (spanning_cell_rect.intersect(cell_rect).get_area()
                        / cell_rect.get_area()) > 0.5:
                    cell['subcell'] = True
                    break

            if cell['subcell']:
                subcells.append(cell)
            else:
                # cell text = extract_text_inside_bbox(table_spans,
                # cell['bbox'])
                # cell['cell text'] = cell text
                cell['projected row header'] = False
                cells.append(cell)

    for spanning_cell in spanning_cells:
        spanning_cell_rect = Rect(list(spanning_cell['bbox']))
        cell_columns = set()
        cell_rows = set()
        cell_rect = None
        header = True
        for subcell in subcells:
            subcell_rect = Rect(list(subcell['bbox']))
            subcell_rect_area = subcell_rect.get_area()
            if (subcell_rect.intersect(spanning_cell_rect).get_area()
                    / subcell_rect_area) > 0.5:
                if cell_rect is None:
                    cell_rect = Rect(list(subcell['bbox']))
                else:
                    cell_rect.include_rect(Rect(list(subcell['bbox'])))
                cell_rows = cell_rows.union(set(subcell['row_nums']))
                cell_columns = cell_columns.union(set(subcell['column_nums']))
                # By convention here, all subcells must be classified
                # as header cells for a spanning cell to be classified
                # as a header cell;
                # otherwise, this could lead to a non-rectangular header region
                header = header and 'column header' in subcell and subcell[
                    'column header']
        if len(cell_rows) > 0 and len(cell_columns) > 0:
            cell = {'bbox': list(cell_rect),
                    'column_nums': list(cell_columns),
                    'row_nums': list(cell_rows),
                    'column header': header,
                    'projected row header': spanning_cell[
                        'projected row header']}
            cells.append(cell)

    # Compute a confidence score based on how well the page tokens
    # slot into the cells reported by the model
    _, _, cell_match_scores = postprocess.slot_into_containers(cells, [])
    try:
        mean_match_score = sum(cell_match_scores) / len(cell_match_scores)
    except ZeroDivisionError:
        confidence_score = 0
    else:
        min_match_score = min(cell_match_scores)
        confidence_score = (mean_match_score + min_match_score)/2

    # Dilate rows and columns before final extraction
    # dilated_columns = fill_column_gaps(columns, table_bbox)
    dilated_columns = columns
    # dilated_rows = fill_row_gaps(rows, table_bbox)
    dilated_rows = rows
    for cell in cells:
        column_rect = Rect()
        for column_num in cell['column_nums']:
            column_rect.include_rect(list(dilated_columns[column_num]['bbox']))
        row_rect = Rect()
        for row_num in cell['row_nums']:
            row_rect.include_rect(list(dilated_rows[row_num]['bbox']))
        cell_rect = column_rect.intersect(row_rect)
        cell['bbox'] = list(cell_rect)

    span_nums_by_cell, _, _ = postprocess.slot_into_containers(
        cells,
        [],
        overlap_threshold=0.001,
        unique_assignment=True,
        forced_assignment=False
        )
    for cell, cell_span_nums in zip(cells, span_nums_by_cell):
        cell_spans = []
        # Refine how text is extracted;
        # should be character-based, not span-based;
        # but need to associate
        cell['cell text'] = postprocess.extract_text_from_spans(
            cell_spans,
            remove_integer_superscripts=False)
        cell['spans'] = cell_spans
    # Adjust the row, column, and cell bounding boxes
    # to reflect the extracted text
    num_rows = len(rows)
    rows = postprocess.sort_objects_top_to_bottom(rows)
    num_columns = len(columns)
    columns = postprocess.sort_objects_left_to_right(columns)
    min_y_values_by_row = defaultdict(list)
    max_y_values_by_row = defaultdict(list)
    min_x_values_by_column = defaultdict(list)
    max_x_values_by_column = defaultdict(list)
    for cell in cells:
        min_row = min(cell["row_nums"])
        max_row = max(cell["row_nums"])
        min_column = min(cell["column_nums"])
        max_column = max(cell["column_nums"])
        for span in cell['spans']:
            min_x_values_by_column[min_column].append(span['bbox'][0])
            min_y_values_by_row[min_row].append(span['bbox'][1])
            max_x_values_by_column[max_column].append(span['bbox'][2])
            max_y_values_by_row[max_row].append(span['bbox'][3])
    for row_num, row in enumerate(rows):
        if len(min_x_values_by_column[0]) > 0:
            row['bbox'][0] = min(min_x_values_by_column[0])
        if len(min_y_values_by_row[row_num]) > 0:
            row['bbox'][1] = min(min_y_values_by_row[row_num])
        if len(max_x_values_by_column[num_columns-1]) > 0:
            row['bbox'][2] = max(max_x_values_by_column[num_columns-1])
        if len(max_y_values_by_row[row_num]) > 0:
            row['bbox'][3] = max(max_y_values_by_row[row_num])
    for column_num, column in enumerate(columns):
        if len(min_x_values_by_column[column_num]) > 0:
            column['bbox'][0] = min(min_x_values_by_column[column_num])
        if len(min_y_values_by_row[0]) > 0:
            column['bbox'][1] = min(min_y_values_by_row[0])
        if len(max_x_values_by_column[column_num]) > 0:
            column['bbox'][2] = max(max_x_values_by_column[column_num])
        if len(max_y_values_by_row[num_rows-1]) > 0:
            column['bbox'][3] = max(max_y_values_by_row[num_rows-1])
    for cell in cells:
        row_rect = Rect()
        column_rect = Rect()
        for row_num in cell['row_nums']:
            row_rect.include_rect(list(rows[row_num]['bbox']))
        for column_num in cell['column_nums']:
            column_rect.include_rect(list(columns[column_num]['bbox']))
        cell_rect = row_rect.intersect(column_rect)
        if cell_rect.get_area() > 0:
            cell['bbox'] = list(cell_rect)

    return cells, confidence_score


def cells_to_csv(cells):
    """
    Convert cells information to Pandas DataFrame format.
    """
    if len(cells) > 0:
        num_columns = max([max(cell['column_nums']) for cell in cells]) + 1
        num_rows = max([max(cell['row_nums']) for cell in cells]) + 1
    else:
        return

    header_cells = [cell for cell in cells if cell['column header']]
    if len(header_cells) > 0:
        max_header_row = max([max(cell['row_nums']) for cell in header_cells])
    else:
        max_header_row = -1

    table_array = np.empty([num_rows, num_columns], dtype="object")
    if len(cells) > 0:
        for cell in cells:
            for row_num in cell['row_nums']:
                for column_num in cell['column_nums']:
                    table_array[row_num, column_num] = cell["cell text"]

    header = table_array[:max_header_row + 1, :]
    flattened_header = []
    for col in header.transpose():
        flattened_header.append(' | '.join(OrderedDict.fromkeys(col)))
    df = pd.DataFrame(table_array[max_header_row+1:, :],
                      index=None, columns=flattened_header)

    return df.to_csv(index=None)


def cells_to_html(cells):
    """
    Convert cells information into HTML Structure.
    """
    cells = sorted(cells, key=lambda k: min(k['column_nums']))
    cells = sorted(cells, key=lambda k: min(k['row_nums']))

    table = ET.Element("table")
    table.set("border", "1")
    current_row = -1

    for cell in cells:
        this_row = min(cell['row_nums'])

        attrib = {}
        colspan = len(cell['column_nums'])
        if colspan > 1:
            attrib['colspan'] = str(colspan)
        rowspan = len(cell['row_nums'])
        if rowspan > 1:
            attrib['rowspan'] = str(rowspan)
        if this_row > current_row:
            current_row = this_row
            if cell['column header']:
                cell_tag = "th"
                row = ET.SubElement(table, "thead")
            else:
                cell_tag = "td"
                row = ET.SubElement(table, "tr")
        tcell = ET.SubElement(row, cell_tag, attrib=attrib)
        tcell.text = cell['cell text']

    return str(ET.tostring(table, encoding="unicode",
                           short_empty_elements=False))


def visualize_cells(img, cells, show_plot=True):
    """
    Visualize cells header, rows, spanning cells and returns the plot.

    Arguments:
    img: PIL.Image format, the image of the table.
    cells: list of dict, the cells information,
    in this case, it would be the 'cells' output of `recognize()` function.
    e.g. `cells = extracted_tables['cells'][0]`
    show_plot: bool, whether to show the plot in a new Matplotlib window
    Returns:
    new_img: PIL.Image format, the table with the cells colored and segmented.
    """
    plt.imshow(img, interpolation="lanczos")
    plt.gcf().set_size_inches(20, 20)
    ax = plt.gca()
    
    for cell in cells:
        bbox = cell['bbox']

        if cell['column header']:
            facecolor = (1, 0, 0.45)
            edgecolor = (1, 0, 0.45)
            alpha = 0.3
            linewidth = 2
            hatch = '//////'
        elif cell['projected row header']:
            facecolor = (0.95, 0.6, 0.1)
            edgecolor = (0.95, 0.6, 0.1)
            alpha = 0.3
            linewidth = 2
            hatch = '//////'
        else:
            facecolor = (0.3, 0.74, 0.8)
            edgecolor = (0.3, 0.7, 0.6)
            alpha = 0.3
            linewidth = 2
            hatch = '\\\\\\\\\\\\'
 
        rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1],
                                 linewidth=linewidth,
                                 edgecolor='none',
                                 facecolor=facecolor,
                                 alpha=0.1)
        ax.add_patch(rect)
        rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1],
                                 linewidth=linewidth,
                                 edgecolor=edgecolor,
                                 facecolor='none',
                                 linestyle='-',
                                 alpha=alpha)
        ax.add_patch(rect)
        rect = patches.Rectangle(bbox[:2], bbox[2]-bbox[0], bbox[3]-bbox[1],
                                 linewidth=0,
                                 edgecolor=edgecolor,
                                 facecolor='none',
                                 linestyle='-',
                                 hatch=hatch,
                                 alpha=0.2)
        ax.add_patch(rect)

    plt.xticks([], [])
    plt.yticks([], [])

    legend_elements = [Patch(facecolor=(0.3, 0.74, 0.8),
                             edgecolor=(0.3, 0.7, 0.6),
                             label='Data cell', hatch='\\\\\\\\\\\\',
                             alpha=0.3),
                       Patch(facecolor=(1, 0, 0.45), edgecolor=(1, 0, 0.45),
                             label='Column header cell', hatch='//////',
                             alpha=0.3),
                       Patch(facecolor=(0.95, 0.6, 0.1),
                             edgecolor=(0.95, 0.6, 0.1),
                             label='Projected row header cell', hatch='//////',
                             alpha=0.3)]
    plt.legend(handles=legend_elements,
               bbox_to_anchor=(0.5, -0.02),
               loc='upper center', borderaxespad=0,
               fontsize=10, ncol=3)
    plt.gcf().set_size_inches(10, 10)
    plt.tight_layout()
    plt.margins(0, 0)
    plt.axis('off')
    # If show plot is true, open a new Matplotlib window and show it
    if show_plot:
        plt.show()
    # Render the figure as an RGBA array
    canvas = agg.FigureCanvasAgg(plt.gcf())
    canvas.draw()
    buf = canvas.buffer_rgba()
    # Convert the RGBA array to a PIL image
    new_img = Image.fromarray(np.array(buf)).save("table.png")
    print("Table image saved as table.png")

    return new_img


def recognize_text(image: np.ndarray,
                   table: List[Dict],
                   reader: Reader = None,
                   text_threshold: float = 0.7):
    """
    Recognize text cell-by-cell in a table image using OCR.

    Args:
        image: A numpy array representing the table image.
        table: A list of dictionaries representing the table structure,
        in this case it should be
        the output of the `objects_to_structures` function.
            Each dictionary should have the following keys:
                'bbox': A list of four numbers representing the bounding box
                of the cell.
                'cell text': A string representing the text in the cell.
                'spans': A list of dictionaries representing the text spans
                in the cell.
                    Each dictionary should have the following keys:
                        'bbox': A list of four numbers representing the
                        bounding box of the span.
                        'text': A string representing the text in the span.
                        'span_num': An integer representing the span number.
                        'line_num': An integer representing the line number.
                        'block_num': An integer representing the block number.
        reader: An EasyOCR reader object. If None, a default reader
        will be used.
        text_threshold: A float representing the text threshold for the
        OCR reader.

    Returns:
        A list of dictionaries similar to the input argument,
        but the 'cell text' field should be replaced with the OCR result
    """
    if not isinstance(image, np.ndarray):
        raise TypeError("image must be a numpy array")
    if not isinstance(table, list):
        raise TypeError("table must be a list")
    if reader is None:
        WARNING("No OCR reader provided. Using default reader.")
    if not isinstance(reader, Reader):
        raise TypeError("reader must be an EasyOCR reader object")

    for cell in tqdm(table, desc="Processing cells"):
        box = image[int(cell['bbox'][1]):int(cell['bbox'][3]),
                    int(cell['bbox'][0]):int(cell['bbox'][2])]
        # Recognize the text
        text = reader.readtext(box,
                               decoder="beamsearch",
                               beamWidth=10,
                               text_threshold=text_threshold,
                               batch_size=8)
        # Concatenate the text
        text = " ".join([str(j[1]) for j in text])
        cell['cell text'] = text
    return table

def write_html(html, path="index.html"):
    """
    Write HTML to a file.
    """
    html = "<html><body>" + html + "</body></html>"
    with open(path, "w") as f:
        f.write(html)
                        

