<<<<<<< HEAD
""" boundingbox.py : Generate bounding box coordinates for the extracted entities """
=======
""" Generate bounding box coordinates for the extracted entities """
>>>>>>> Update DockerFile

import os
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
from enum import Enum
import re
from fuzzywuzzy import fuzz 

# Update path to Google Cloud Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("PATH TO GOOGLE API CREDENTIALS")


def generateboundingbox(image, content, entities):

 
    def drawBoxes(image, bounds, color):
        """
        Definition: Draw bounding boxes on the image from the input list of bounding box coordinates using the appropriate color
        coding, which coressponds to the label(entity)

        Input     : image  - input image
                    bounds - list of bounding box coordinates
                    color  - color coded labels(entities)
                    width  - bounding box line width
        Output    : image overlaid with bounding boxes 
       
        """
        draw = ImageDraw.Draw(image)
        for bound in bounds:
            draw.line([
                bound.vertices[0].x, bound.vertices[0].y,
                bound.vertices[1].x, bound.vertices[1].y,
                bound.vertices[2].x, bound.vertices[2].y,
                bound.vertices[3].x, bound.vertices[3].y,
                bound.vertices[0].x, bound.vertices[0].y], fill=color, width=5)
            
        return image

    class FeatureType(Enum):
        PAGE = 1
        BLOCK = 2
        PARA = 3
        WORD = 4
        SYMBOL = 5

    def getTextandBounds(content):
        """
        Extract text and corresponding bounding box coordinates
        """
    
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image(content=content)            

        response = client.document_text_detection(image=image)
        document = response.full_text_annotation

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
                        # words.append((word, word.bounding_box))    
                    text.append((para, paragraph.bounding_box))
                    
                                            
        return text

    def getBounds(entities, text):
        """
        Extract bounding box coordinates for relevant entities
        """
        box = []
        for entity in entities:
            for token in text:
                if fuzz.partial_ratio(entity, token) > 95:
                    box.append(token[1])

        return box

        textBounds = getTextandBounds()
        
    textBoxes = getTextandBounds(content)
    bounds = getBounds(entities, textBoxes)
    
    outImage = drawBoxes(image, bounds, "blue")

    return outImage
