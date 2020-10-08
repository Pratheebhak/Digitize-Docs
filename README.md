# Digitize-Handwritten-Labels-on-Botanical-Images
Handwritten Labels Extraction and Tagging in Herbarium Images

## Motivation

Museums are manually digitizing millions of imaged documents of Herbarium sheets, which might take decades to complete at the current pace of manual transcription. This repository proposes a model using AI tools to automate the transcription process, to cut down the time significantly and facilitate faster and easier access to resources.

## Installation

Clone the github repository and set biotag as the working directory.
> git clone   
> cd ./biotag

### Requisites
This repository has the following dependencies:
* [Anaconda](https://docs.anaconda.com/anaconda/install/)
* Streamlit
* Google Cloud API Credentials (for OCR)

### Setup

Create a conda virtual environment and install the dependencies

> conda create-n biotag python=3   
> conda activate insight   
> pip install -r requirements.txt   

### Run

> streamlit run app.py




