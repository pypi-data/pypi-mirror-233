import logging
from easyocr import Reader
from .engine.inference import *
from .engine.postprocess import *

class TableExtractionPipeline(object):
    """
    Main pipeline for Table Transformer.
    """
    def __init__(self, model_path, device=None,
                 structure_class_thresholds=None,
                 ocr_model: Reader=None):

        self.str_device = device

        self.str_class_name2idx = get_class_map('structure')
        self.str_class_idx2name = {v: k
                                   for k, v in self.str_class_name2idx.items()}
        self.str_class_thresholds = structure_class_thresholds

        self.ocr_model=None
        if ocr_model is not None:
            logging.info("OCR model is detected")
            self.ocr_model = ocr_model
            if self.str_device != self.ocr_model.device:
                logging.warning("OCR model device is different from the pipeline")
                logging.warning("OCR model will be moved to the pipeline device")
                self.ocr_model.device = self.str_device

        
        if model_path is not None:
            self.str_model = onnxruntime.InferenceSession(model_path)
            print("Structure model initialized.")


    def __call__(self, page_image,
                out_objects=False, out_cells=False,
                out_html=False, out_csv=False):
        return self.recognize(page_image,
                              out_objects=out_objects, out_cells=out_cells,
                              out_html=out_html, out_csv=out_csv)


    def recognize(self, img, out_objects=False, out_cells=False,
                  out_html=False, out_csv=False, text_threshold=0.7) -> Dict:
        """
        Recogize the structure of the table image

        Arguments:
        img: a PIL.Image object containing the table
        tokens: (depreciated) originally text to fill in the tables,
        but it has been depreciated in place of OCR.
        out_objects: bool, to output objects
        out_cells: bool, to output individual cells dictionary
        out_html: bool, to output html format of the extracted table
        out_csv: bool, to output CSV format of the extracted table
        reader: an EasyOCR.Reader object for reading text; if None,
        then text recognition will not be performed.
        text_threshold: threshold confidence for recognizing text
        onnx_inference: bool,
        whether to run ONNX model instead of PyTorch model.

        Return: a dictionary of outputs, depending on the arguments out_objects,
        out_cells, out_html, out_csv are True or not.
        """
        out_formats = {}
        if self.str_model is None:
            print("No structure model loaded.")
            return out_formats

        if not (out_objects or out_cells or out_html or out_csv):
            print("No output format specified")
            return out_formats

        # Transform the image how the model expects it
        img = img.convert('RGB')
        img_tensor = structure_transform(img)

        # Run input image through the model
        np_image = np.expand_dims(
            np.array(img_tensor.to(self.str_device)).astype(np.float32),
            axis=0)
        ort_inputs = {self.str_model.get_inputs()[0].name: np_image}
        ort_output = self.str_model.run(["pred_logits", "pred_boxes"],
                                                ort_inputs)
        outputs = {
            "pred_logits": torch.from_numpy(ort_output[0]),
            "pred_boxes": torch.from_numpy(ort_output[1])
        }

        # Post-process detected objects, assign class labels
        objects = outputs_to_objects(outputs, img.size,
                                     self.str_class_idx2name)
        if out_objects:
            out_formats['objects'] = objects
        if not (out_cells or out_html or out_csv):
            return out_formats

        # Further process the detected objects so they correspond
        # to a consistent table
        tables_structure = objects_to_structures(objects,
                                                 self.str_class_thresholds)

        # Enumerate all table cells: grid cells and spanning cells
        tables_cells = [structure_to_cells(structure)[0]
                        for structure in tables_structure]
        if out_cells:
            out_formats['cells'] = tables_cells
        if not (out_html or out_csv):
            return out_formats

        # Extract text from table cells
        if self.ocr_model is not None:
            img = np.asarray(img)
            # Recognize text in each cell
            for cells in tables_cells:
                cells = recognize_text(image=img,
                                    table=cells,
                                    reader=self.ocr_model,
                                    text_threshold=text_threshold)

        # Convert cells to HTML
        if out_html:
            tables_htmls = [cells_to_html(cells) for cells in tables_cells]
            print(tables_htmls[0])
            write_html(tables_htmls[0], path="index.html")
            print(f"HTML file written to index.html")
            out_formats['html'] = tables_htmls

        # Convert cells to CSV, including flattening multi-row
        # column headers to a single row 
        if out_csv:
            tables_csvs = [cells_to_csv(cells) for cells in tables_cells]
            print(tables_csvs[0])
            out_formats['csv'] = tables_csvs

        return out_formats

