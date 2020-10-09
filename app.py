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
    
  # Input the image url
  url = st.sidebar.text_input("Enter image URL:")

  if url:
    # Download and save the input image   
    saveImage(url)
    st.sidebar.image("inference/input/image.jpg", caption="Input Plant Specimen Image", width=250, channels="RGB")

    # Detect the text regions in the image
    detect.detect()

    # Select the detected images to be passed through the OCR
    imageList = []
    contentList = []
    if len(os.listdir("inference/detection")) == 0:
      # Select images in Output Folder
      filename = "inference/output/*.jpg"
      image = Image.open(filename)
      imageList.append(image)
      st.image(image, width=500, channel='RGB')
      with io.open(filename, 'rb') as imageFile:
        contentList.append(imageFile.read())

    else:
      # Select images in the Detection Folder
      for filename in glob.glob('inference/detection/*.jpg'): 
        image = Image.open(filename)
        imageList.append(image)
        path = (os.path.abspath(filename))
        with io.open(path, 'rb') as imageFile:
          contentList.append(imageFile.read()) 
    
    model = extract.handwrittenText()

    st.subheader("Detected Text Label")
    for image, content in zip(imageList, contentList):      
      st.image(image, width=400, channel='RGB', caption='Detected Text Labels in the Input Image')
      ocrtext, text = ocr.handwrittenOCR(content)
      st.write("OCR Text: ", ocrtext)
      st.write("Processed OCR Text: ", ' '.join([word for word in text]))
      st.subheader("Extracted entities:")

      rawtext = ' '.join([val for val in ocrtext])
      # barcode, year, genus, species, collector, geography = extract.handwrittenText(ocrtext, text)
      year = model.findYear(text)
      collector = model.findCollector(ocrtext)
      geography = model.findGeography(rawtext)
      genus, species = model.findScientificName(text)
      st.write("Scientific Name: ", genus + " " + species)
      st.write("Collector: ", ','.join([val for val in collector]))
      st.write("Geography: ", ','.join([val for val in geography]))
      st.write("Year: ", ','.join([val for val in year]))
    
      

      # entities = list(genus) + list(species) + list(collector) + list(geography)
      # boxImage = box.generateboundingbox(image, content, entities)
      # st.subheader("Tagged entities")
      # st.image(boxImage, width=500, channels='BGR')




      # rawText = ' '.join([word for word in raw])
      # st.write("Raw OCR Text: ",rawText)
      # cleanText = ' '.join([word for word in clean])
      # st.write("OCR Text: ", cleanText)






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
        
    st.sidebar.success('Image sucessfully downloaded')
  else:
    st.sidebar.error('Image couldn\'t be retreived from the URL')

        
if __name__ == "__main__":
  main()
