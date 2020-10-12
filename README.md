# \<biotag\>
Handwritten Labels Extraction and Tagging in Botanical Images

***Parts of Scripts in this repository has been redacted due to copyright reasons***

## Table of Contents

* [About the Project](#about-the-project)
  * [Model](#model)
  * [Object Detection Training Module](#object-detection-training-module)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Optional: Docker](#docker-optional)
* [Acknowledgements](#acknowledgements)
  

## About the Project

Museums are manually digitizing millions of imaged documents of Herbarium sheets, which might take decades to complete at the current pace of manual transcription. This repository proposes a model using AI tools to automate the transcription process, to cut down the time significantly and facilitate faster and easier access to resources.

### Model
The model pipeline can be visualized as follows:
![Model Pipeline](/inference/Model.PNG)

### Object Detection Training Module

YOLOv5 Object Detection Model developed by ultralytics was used to train an object detection model on custom dataset. The model training parameters and results are located in the training directory. The model training was implemented in Google colaboratory and can be accessed via the following link:
* Google Colab with free GPU
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Pratheebhak/biotag/blob/master/training/YOLOv5_Training_Module.ipynb)

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

## Acknowledgements
* [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)





