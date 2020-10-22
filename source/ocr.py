""" Extract OCR text from the input image """
# pylint: disable=no-member

import os
import io
from google.cloud import vision
import re
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import imutils
import cv2

# Google Cloud Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser(
    "PATH TO GOOGLE API CREDENTIALS"
)


class handwrittenOCR:
    def ocrText(self, content):
        """
        Extract the raw OCR text from the input image using Google Cloud Vision API
        """
        try:

            client = vision.ImageAnnotatorClient()
            image = vision.types.Image(content=content)

            response = client.document_text_detection(image=image)
            document = response.full_text_annotation
            textdoc = document.text

            text = []

            breaks = vision.enums.TextAnnotation.DetectedBreak.BreakType
            for page in document.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        para = ""
                        line = ""
                        for word in paragraph.words:
                            for symbol in word.symbols:
                                line += symbol.text
                                if symbol.property.detected_break.type == breaks.SPACE:
                                    line += " "
                                if (
                                    symbol.property.detected_break.type
                                    == breaks.EOL_SURE_SPACE
                                ):
                                    line += " "
                                    para += line
                                    line = ""
                                if (
                                    symbol.property.detected_break.type
                                    == breaks.LINE_BREAK
                                ):
                                    para += line
                                    line = ""

                        text.append(para)

            return text, textdoc

        except Exception as e:
            print(e)
            return None, None

    def processText(self, rawText):
        """
        Preprocess the raw OCR text for fuzzymatching/entity recognition
        """
        text = " ".join([string for string in rawText])
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = text.split()
        return text
