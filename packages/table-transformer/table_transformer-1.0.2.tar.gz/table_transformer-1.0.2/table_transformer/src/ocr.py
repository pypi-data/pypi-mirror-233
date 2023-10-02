"""
Initialize OCR Model
"""
from typing import List
from easyocr import Reader
import numpy as np
from PIL.Image import Image


class OCR(Reader):
    """
    OCR Object
    """

    def get_text(self, img: Image, text_threshold: float) -> List:
        """
        Get text from an image
        :param img: PIL image
        """

        img = np.array(img)
        # img is a numpy array for your RGB image
        ocr_result = self.readtext(img, width_ths=.03,
                                   text_threshold=text_threshold)

        tokens = []
        for i, res in enumerate(ocr_result):
            tokens.append({
                "bbox": list(map(int, [res[0][0][0], res[0][0][1],
                                       res[0][2][0], res[0][2][1]])),
                "text": res[1],
                "flags": 0,
                "span_num": i,
                "line_num": 0,
                "block_num": 0
            })

        return tokens
