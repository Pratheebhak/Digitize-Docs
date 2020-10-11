""" Streamlit app for the biotag model """

import os
import streamlit as st
import biotag.detect as detect
import biotag.ocr as ocr
import biotag.extract as extract
import biotag.boundingbox as box
import requests 
import shutil 
from PIL import Image
import glob
import io


def main():
  
  st.title("</biotag>")
  st.header("Handwritten Label Extraction on Botanical Images")
  st.write("</biotag> detects the handwritten plant specimen labels on botanical images, \
    converts the imaged text into digital format and \
    extracts and categorizes useful information in the text.")
    
      

def saveImage(image_url):
  " Download and save the image from the given URL "

  path = "inference/input"

  # Path exists: Delete the folder and create a new folder
  if os.path.exists(path):
    shutil.rmtree(path)  
  os.makedirs(path)

  filename = "inference/input/image.jpg"

  # Open the url image, set stream to True, this will return the stream content.
  r = requests.get(image_url, stream = True)

  # Check if the image was retrieved successfully
  if r.status_code == 200:
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    r.raw.decode_content = True
    
    # Open a local file with wb ( write binary ) permission.
    with open(filename,'wb') as f:
      shutil.copyfileobj(r.raw, f)
        
    st.sidebar.success('Image sucessfully downloaded')
  else:
    st.sidebar.error('Image couldn\'t be retreived from the URL')

        
if __name__ == "__main__":
  main()
