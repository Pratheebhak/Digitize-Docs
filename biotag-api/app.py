from flask import Flask, request, jsonify

# Create a Flask API
app = Flask(__name__)
app.config["DEBUG"] = True

# Create Routes
@app.route('/', methods=['GET'])
def home():
    return "<h1> biotag-API </h1><p>Handwritten Label Extraction on Botanical Images</p>"


app.run()