import os
import streamlit as st
import source.detect as detect
import source.ocr as ocr
import source.extract as extract
import source.boundingbox as box
import requests 
import shutil 
from PIL import Image
import glob
import io


def main():
  st.title("</biotag>")
  st.header("Handwritten Label Extraction and Tagging on Botanical Images")

  # Input the image url
  url = st.sidebar.text_input("Enter image URL:")

  if url:
    # Download and save the input image
    saveImage(url)
    st.spinner("Downloading the image...")   
    st.sidebar.image("inference/input/image.jpg", caption="Input Plant Specimen Image", width=250, channels="RGB")

    # Detect the text regions in the image
    detect.detect()

    imageList = []
    contentList = []
    for filename in glob.glob('inference/detection/*.jpg'): #assuming gif
      image = Image.open(filename)
      imageList.append(image)
      path = (os.path.abspath(filename))
      with io.open(path, 'rb') as imageFile:
        contentList.append(imageFile.read()) 

    st.subheader("Detected Text Regions in the Input Image:")
    for image in imageList:
      st.image(image, width=400, channel='RGB')
      
    for content in contentList:
      st.subheader("Handwritten Text Detection using OCR...")
      raw, clean = ocr.handwrittenOCR(content)
      st.subheader("Extracting entities from the image...")
      barcode, year, genus, species, collector, geography = extract.handwrittenText(raw, clean)

      st.write("Barcode: ", ','.join([val for val in barcode]))
      st.write("Scientific Name: ", genus + " " + species)
      st.write("Year: ", ','.join([val for val in year]))
      st.write("Collector: ", ','.join([val for val in collector]))
      st.write("Geography: ", ','.join([val for val in geography]))




    # Extract the OCR text from the handwritten image

    # if url:
    #     image, raw, clean = ocr.handwrittenOCR(url)

    #     st.image(image, width=500, channels='BGR')
            
    #     # Extract Entities
    #     # model = extract.handwrittenText()
    #     # # st.write("Barcode: ", model.findBarcode(clean))
    #     # st.write("Scientific Name: ", model.findScientificName(clean))
    #     # st.write("Year: ", model.findYear(clean))
    #     # st.write("Collector: ", model.findCollector(raw))
    #     # st.write("Geography: ", model.findGeography(raw))

    #     st.write("Extracting entities from the image...")
    #     barcode, year, genus, species, collector, geography = extract.handwrittenText(raw, clean)

    #     st.write("Barcode: ", ','.join([val for val in barcode]))
    #     st.write("Scientific Name: ", genus + " " + species)
    #     st.write("Year: ", ','.join([val for val in year]))
    #     st.write("Collector: ", ','.join([val for val in collector]))
    #     st.write("Geography: ", ','.join([val for val in geography]))


    #     # entities = barcode + list(year) + list(genus) + list(species) + list(collector) + list(geography)
    #     # boxImage = box.generateboundingbox(url, entities)
    #     # st.image(boxImage, width=500, channels='BGR')

    #     rawText = ' '.join([word for word in raw])
    #     st.write("Raw OCR Text: ",rawText)
    #     cleanText = ' '.join([word for word in clean])
    #     st.write("OCR Text: ", cleanText)    

def saveImage(image_url):
  """
  Download and save the image from the given URL
  """

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
        
    st.write('Image sucessfully downloaded from the URL: ',filename)
  else:
    st.write('Image couldn\'t be retreived from the URL')

        
if __name__ == "__main__":
  main()
