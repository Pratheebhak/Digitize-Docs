""" Extract entities from the handwritten OCR text """
""" Parts of code redacted due to copyright """


import spacy
import pandas as pd
import re
import jellyfish
from fuzzywuzzy import fuzz


class handwrittenText:

    nlp = spacy.load("en_core_web_sm")

    # Load the input data into dataframes
    dfGenus = pd.read_csv("data/genus_combined.txt", header=None)
    dfSpecies = pd.read_csv("data/plant_species.csv")

    # Preprocess the textual information in the dataframes
    dfGenus.columns = ["genus"]
    dfGenus["genus"] = dfGenus["genus"].str.replace(r"\(.*\)", "")
    dfGenus["genus"] = dfGenus["genus"].str.lower()
    dfGenus["genus"] = dfGenus["genus"].str.rstrip()
    genusList = dfGenus["genus"].to_list()

    dfSpecies["species"] = dfSpecies["species"].str.lower()
    speciesset = set(dfSpecies["species"].dropna().unique().tolist())
    speciesList = list(speciesset)
    dfSpecies["genus"] = dfSpecies["genus"].str.lower()

    # Create a dictionary using the dataframes
    # key   : genus
    # values: list of species associated with the genus
    namesDictionary = {key: [] for key in set(genusList)}

    for index in range(len(dfSpecies)):
        if dfSpecies.loc[index, "genus"] in namesDictionary:
            namesDictionary[dfSpecies.loc[index, "genus"]].append(
                dfSpecies.loc[index, "species"]
            )

    # Load and preprocess countries and states input text files
    dfCountries = pd.read_csv("data/countries.txt", header=None)
    countries = dfCountries[0].to_list()
    countries = [x.lower() for x in countries]

    dfStates = pd.read_csv("data/states.csv")
    states = dfStates["State"].to_list()
    states = [x.lower() for x in states]

    def findBarcode(self, text):
        """
        Extract barcode(s) from the processed text
        """
        barcodes = []
        for string in text:
            if string.isdigit() and len(string) == 8:
                if len(set(string)) == 1:
                    break
                barcodes.append(string)
        return barcodes

    def findYear(self, text):
        """
        Extract year(s) from the processed text
        """
        years = []
        for string in text:
            if string.isdigit() and len(string) == 4:
                if re.search(r"1[8-9]\d\d", string):
                    years.append(string)
                if re.search(r"20[0-2]\d", string):
                    years.append(string)

        return list(set(years))

    def findScientificName(self, text):
        """
        Extract scientific name(s) (genus + species) from the processed text
        Code Redacted
        """

    def findCollector(self, text):
        """
        Extract the collector's name from the OCR text using NER tags and pattern matching
        """
        doc = self.nlp(str(text))
        collectors = []
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                if re.search(r"\w\.\s\w\.\s\w+", ent.text):
                    collectors.append(ent.text)
                if re.search(r"\w\.\s\w\.\s\w\.\s\w+", ent.text):
                    collectors.append(ent.text)
                if re.search(r"\w+\w\.\s\w+", ent.text):
                    collectors.append(ent.text)
                if re.search(r"^\w+\s\w\.\s\w+", ent.text):
                    collectors.append(ent.text)
                if re.search(r"^coll", ent.text):
                    collectors.append(ent.text)
                if re.search(r"^Coll", ent.text):
                    collectors.append(ent.text)

        return collectors

    def findGeography(self, text):
        """
        Extract the collector's name from the OCR text using NER tags and pattern matching
        """
        text = " ".join([x for x in text])
        doc = self.nlp(text)
        geography = []
        for ent in doc.ents:
            if ent.label_ == "GPE" or ent.label_ == "LOC":
                if ent.text.lower() in self.countries:
                    geography.append(ent.text)
                if ent.text.lower() in self.states:
                    geography.append(ent.text + " US")

        text1 = text.split()

        for token in text1:
            for country in self.countries:
                if fuzz.ratio(token, country) > 90:
                    geography.append(token)
            for state in self.states:
                if fuzz.ratio(token, state) > 90:
                    geography.append(token + " US")

        return list(set(geography))
