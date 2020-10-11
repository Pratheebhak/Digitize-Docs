from flask import Flask, request, jsonify

# Create a Flask API
app = Flask(__name__)
app.config["DEBUG"] = True

# Create Routes
@app.route('/', methods=['GET'])
def home():
    return "<h1>Handwritten Label Extraction on Botanical Images</h1>"

# Single Printed Image URL
@app.route('/single_printed', methods=['GET','POST'])
def single_printed():
    url = request.get_json()

# Single Printed Image URL
@app.route('/single_handwritten', methods=['GET','POST'])
def single_handwritten():
    url = request.get_json()


# Multiple Printed Image URLs
@app.route('/multiple_printed', methods=['GET','POST'])
def multiple_printed():
    url = request.get_json()



# Multiple Printed Image URLs
@app.route('/multiple_handwritten', methods=['GET','POST'])
def multiple_handwritten():
    url = request.get_json()


if __name__ = '__main__':
    app.run()