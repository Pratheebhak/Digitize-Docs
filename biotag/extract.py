"""
Title       : extract.py
Definition  : Extracts entities from the processed OCR text
Input       : raw OCR text
Output      : entities
"""

import spacy
import pandas as pd
import re
import jellyfish
from fuzzywuzzy import fuzz

