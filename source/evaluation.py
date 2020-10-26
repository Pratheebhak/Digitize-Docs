""" Entity Extraction from OCR text Analysis """

import extract as extract
import ocr as ocr
import pandas as pd
import numpy as np

# Read the csv file to be evaluated
df = pd.read_csv("data/ocrdata.csv")

# Process Text
ocrmodel = ocr.handwrittenOCR()
df["Processed Text"] = df["OCR Text"].apply(ocrmodel.processText)
df["Processed Text"] = df["Processed Text"].split()

# Predict the entities from the input OCR text
model = extract.handwrittenText()
df["Predicted Scientific Name"] = (
    df["Processed Text"].dropna().apply(model.findScientificName)
)
df["Predicted Geography"] = df["Processed Text"].dropna().apply(model.findGeography)
df["Predicted Collector"] = df["Processed Text"].dropna().apply(model.findCollector)
df["Predicted Year"] = df["Processed Text"].dropna().apply(model.findYear)

# Calculate the number of approximately matched entities
df["Barcode Matches"] = np.where(df["Barcode"] == df["Predicted Barcode"], True, False)
df["Scientific Name Matches"] = np.where(
    fuzz.partial_ratio(df["Scientific Name"], df["Predicted Scientific Name"]) == 100,
    True,
    False,
)
df["Geography Matches"] = np.where(
    fuzz.partial_ratio(df["Geography"], df["Predicted Geography"]) == 100, True, False
)
df["Collector Matches"] = np.where(
    fuzz.partial_ratio(df["Collector"], df["Predicted Collector"]) == 100, True, False
)
df["Year Matches"] = np.where(
    fuzz.partial_ratio(df["Year"], df["Predicted Year"]) == 100, True, False
)

# Calculate and Print Accuracy for each entity
barcode_accuracy = df["Barcode Matches"].values.sum() / df.shape[0]
scientific_name_accuracy = df["Scientific Name Matches"].values.sum() / df.shape[0]
geography_accuracy = df["Geography Matches"].values.sum() / df.shape[0]
collector_accuracy = df["Collector Matches"].values.sum() / df.shape[0]
year_accuracy = df["Year Matches"].values.sum() / df.shape[0]

# Print the accuracies
print("******************Accuracy******************")
print("Barcode          : {:}".format(barcode_accuracy))
print("Scientific Name  : {:}".format(scientific_name_accuracy))
print("Geography        : {:}".format(geography_accuracy))
print("Collector        : {:}".format(collector_accuracy))
print("Year             : {:}".format(year_accuracy))


# Export the predicted results to a csv file
outfile = "/data/outputocr.csv"
df.to_csv(outfile, index=True)
