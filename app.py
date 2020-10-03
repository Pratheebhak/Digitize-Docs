import streamlit as st
import model.ocr as ocr
import model.extract as extract
import model.boundingbox as box

#import model.helper as helper

def main():
    st.title("Handwritten Field Extraction on botanical Images")

    # Input the image url
    url = st.text_input("Enter url:")
    st.write("Loading the image...")
    # Extract the OCR text from the handwritten image
    if url:
        image, raw, clean = ocr.handwrittenOCR(url)

        st.image(image, width=500, channels='BGR')
            
        # Extract Entities
        # model = extract.handwrittenText()
        # # st.write("Barcode: ", model.findBarcode(clean))
        # st.write("Scientific Name: ", model.findScientificName(clean))
        # st.write("Year: ", model.findYear(clean))
        # st.write("Collector: ", model.findCollector(raw))
        # st.write("Geography: ", model.findGeography(raw))

        st.write("Extracting entities from the image...")
        barcode, year, genus, species, collector, geography = extract.handwrittenText(raw, clean)

        st.write("Barcode: ", ','.join([val for val in barcode]))
        st.write("Scientific Name: ", genus + " " + species)
        st.write("Year: ", ','.join([val for val in year]))
        st.write("Collector: ", ','.join([val for val in collector]))
        st.write("Geography: ", ','.join([val for val in geography]))


        # entities = barcode + list(year) + list(genus) + list(species) + list(collector) + list(geography)
        # boxImage = box.generateboundingbox(url, entities)
        # st.image(boxImage, width=500, channels='BGR')

        rawText = ' '.join([word for word in raw])
        st.write("Raw OCR Text: ",rawText)
        cleanText = ' '.join([word for word in clean])
        st.write("OCR Text: ", cleanText)    


        
if __name__ == "__main__":
  main()
