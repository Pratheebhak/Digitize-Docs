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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("PATH TO GOOGLE API CREDENTIALS")

def handwrittenOCR(content):

    def ocrText(content):
        """
        Extract the raw OCR text from the input image using Google Cloud Vision API
        """

        try:
            # img = imutils.url_to_image(url)
        
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # img_pil = Image.fromarray(img)


            # imgByteArr = BytesIO()
            # img_pil.save(imgByteArr, format='PNG', quality = 50, optimize = True)
            # context = imgByteArr.getvalue()

            # with io.open(path, 'rb') as image_file:
            #     content = image_file.read()
           
            client = vision.ImageAnnotatorClient()
            image = vision.types.Image(content=content)            

            response = client.document_text_detection(image=image)
            document = response.full_text_annotation
            textdoc = document.text

            # ocr = []
            # keys = ['description', 'boundingBox', 'confidence', 'entity']
            # chunks = dict.fromkeys(keys)
            text = []
    
            breaks = vision.enums.TextAnnotation.DetectedBreak.BreakType
            for page in document.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        para = ''
                        line = ''
                        for word in paragraph.words:
                            for symbol in word.symbols:
                                line += symbol.text
                                if symbol.property.detected_break.type == breaks.SPACE:
                                    line += ' '
                                if symbol.property.detected_break.type == breaks.EOL_SURE_SPACE:
                                    line += ' '
                                    para += line
                                    line = ''
                                if symbol.property.detected_break.type == breaks.LINE_BREAK:
                                    para += line
                                    line = ''                    
                        
                        text.append(para)
                # chunks['description'] = para
                # ocr.append([chunks])
            return text, textdoc

        except Exception as e:
            print(e)
            return None, None

    def processText(rawText):
        """
        Preprocess the raw OCR text for fuzzymatching/entity recognition
        """
        text = ' '.join([string for string in rawText])
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)  
        text = text.split() 
        # # Remove the irrelevant information from the color palette in images
        # irrelevantList = ['0','1','2','3','4','5','6','7','8','9','10','cm','copyright','provided','is','the','a','by','harvard','herbarium',
        #             'university','reserved']
        # text = [string for string in text if string not in irrelevantList]
        return text

    
    textpara, textdoc = ocrText(content)
    cleanText = processText(textpara)
   

    return  textdoc, cleanText
