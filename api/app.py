""" API for the model """

from flask import Flask, request, jsonify

# Create a Flask API
app = Flask(__name__)
app.config["DEBUG"] = True

# Create Routes
@app.route('/', methods=['GET'])
def home():
    return "<h1>Handwritten Label Extraction on Botanical Images</h1>"


if __name__ = '__main__':
    app.run()