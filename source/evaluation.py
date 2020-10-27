""" Entity Extraction from OCR text Analysis """

import extract as extract
import ocr as ocr
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

# Read the csv file to be evaluated
df = pd.read_csv("data/ocrdata.csv")

# Process Text
df["Processed Text"] = df["OCR Text"].str.split()
ocrmodel = ocr.handwrittenOCR()
df["Processed Text"] = df["Processed Text"].apply(ocrmodel.processText)


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
df["Scientific Name Matches"] = df.apply(
    lambda x: fuzz.partial_ratio(x["Scientific Name"], x["Predicted Scientific Name"]),
    axis=1,
)
df["Geography Matches"] = df.apply(
    lambda x: fuzz.partial_ratio(x["Geography"], x["Predicted Geography"]),
    axis=1,
)
df["Collector Matches"] = df.apply(
    lambda x: fuzz.partial_ratio(x["Collector"], x["Predicted Collector"]),
    axis=1,
)
df["Year Matches"] = df.apply(
    lambda x: fuzz.partial_ratio(x["Year"], x["Predicted Year"]),
    axis=1,
)

# Calculate and Print Accuracy for each entity
barcode_accuracy = 100 * df["Barcode Matches"].values.sum() / df.shape[0]
scientific_name_accuracy = df["Scientific Name Matches"].mean(skipna=True)
geography_accuracy = df["Geography Matches"].mean(skipna=True)
collector_accuracy = df["Collector Matches"].mean(skipna=True)
year_accuracy = df["Year Matches"].mean(skipna=True)

# Print the accuracies
print("******************Accuracy******************")
print("Barcode          : {:}".format(barcode_accuracy))
print("Scientific Name  : {:}".format(scientific_name_accuracy))
print("Geography        : {:}".format(geography_accuracy))
print("Collector        : {:}".format(collector_accuracy))
print("Year             : {:}".format(year_accuracy))


# Export the predicted results to a csv file
outfile = "data/outputocr.csv"
df.to_csv(outfile, index=True)
