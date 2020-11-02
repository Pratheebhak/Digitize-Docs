# \<biotag\>
Handwritten Labels Extraction and Tagging in Botanical Images

***Data and Parts of Scripts in this repository has been redacted due to copyright reasons***

## Table of Contents

* [About the Project](#about-the-project)
  * [Model](#model)
  * [Demo](#demo)
  * [Object Detection Training Module](#object-detection-training-module)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Optional: Docker](#docker-optional)
* [Directory Structure](#directory-structure)
* [References](#references)
  

## About the Project

Museums are manually digitizing millions of imaged documents of Herbarium sheets, which might take decades to complete at the current pace of manual transcription. This repository proposes a model using cutting-edge AI tools to automate the transcription process, to cut down the time significantly and facilitate faster and easier access to resources. 

### Model
The pipeline consists of three stages and can be visualized as shown below:
* Object Detection : To detect the desirable i.e., text and barcode regions in the input botanical image.
* Optical Character Recognition : To recognize and extract the text in the handwritten text regions.
* Entity Extraction: To extract the entities from the extracted OCR text.A set of algorithms are adopted for accurately extracting the entities from the OCR text and are listed as follows:
  * Fuzzy Matching: Group of techniques used to match strings based on a pattern or set of rules
  * [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) is the metric used to measure string similarity
  * Named Entity Recognition and Rule based Matching
<p align="center">
  <img src="https://github.com/Pratheebhak/biotag/blob/master/images/Model.PNG" alt="Model Pipeline"/>
</p>

### Demo
The streamlit app demo of the model is demonstrated using the following gif:
<p align="center">
  <img src="https://github.com/Pratheebhak/biotag/blob/master/images/finaldemo.gif" alt="<biotag> Demo"/>
</p>


### Object Detection Training Module

YOLOv5 Object Detection Model developed by ultralytics was used to train an object detection model on custom dataset. The model training parameters and results are located in the training directory. The model training was implemented in Google colaboratory and can be accessed via the following link:
* Google Colab with free GPU
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Pratheebhak/biotag/blob/master/source/training/YOLOv5_Training_Module.ipynb)

## Getting Started

Clone the github repository and set biotag as the working directory.
```
git clone https://github.com/Pratheebhak/biotag.git   
cd ./biotag
```

### Prerequisites
This repository has the following dependencies:
* [Anaconda](https://docs.anaconda.com/anaconda/install/)
* Streamlit
* Google Cloud API Credentials (for OCR)

### Installation

Create a conda virtual environment and install the dependencies
```
conda create-n biotag python=3   
conda activate biotag   
pip install -r requirements.txt   
```
To run the Streamlit app,
```
cd ./source
streamlit run app.py
```

### Docker (Optional)
To containerize the Streamlit app,
* Install Docker [Desktop](https://www.docker.com/products/docker-desktop) or [Engine](https://docs.docker.com/engine/)
* Run the following commands for docker build and run
```
docker build -t biotag-streamlit:v1 -f DockerFile .
docker run -p 8501:8501 biotag-streamlit:v1
```
## Directory Structure

```
.
├── source
│   ├── data               - Redacted due to copyrights
│   └── inference          - Object Detection Images         
│       ├── input          - input image       
│       ├── output         - output image with bounding boxes, bounding box coordinates of the detected objects
│       └── detection      - cropped images of the detected text regions in the output image
│   ├── models             - Object Detection helper module
│   ├── training           - Object Detection Training Module Logs
│   ├── utils              - Object Detection helper module
│   ├── app.py             - Streamlit app interface for the model
│   ├── boundingbox.py     - Generates bounding boxes for the extracted entities
│   ├── detect.py          - Detects the desired text regions in the input image URL
│   ├── evaluation.py      - Fuzzy Matching Entity Extraction Analysis
│   ├── extract.py         - Extracts entities from the OCR text
│   └── ocr.py             - Extracts OCR text from the detected text regions
├── images
│   └── README images
├── .gitignore
├── DockerFile             - Docker file for the Streamlit app
├── README.md              - README Markdown File
└── requirements.txt       - Dependencies

```

## References
* [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)





