# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os

from flask import Flask, abort
from flask_cors import CORS
from stockAnalyze import getCompanyStockInfo
from analyze import analyzeText, get_json_stock_data
import json
import requests
from flask import request, jsonify


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/health')
def hello_world():
    return 'Flask server is up and running'

@app.route('/analyze-stock/<ticker>', methods=['GET'])
def analyzeStock(ticker):
    use_mock_json = True
    mock_json_path = './test/result.json'
    stockDataTest = ""

    # Check if mock mode is on AND the file physically exists on the disk
    if use_mock_json and os.path.exists(mock_json_path):
        stockDataTest = get_json_stock_data(mock_json_path)
        return stockDataTest # local json file for testing, replace with live API call when ready

    if len(ticker) > 5 or not ticker.isidentifier():
        abort(400, 'Invalid ticker symbol')
    try:
        analysis = getCompanyStockInfo(ticker)
    except NameError as e:
        abort(404, e)  
    except:
        abort(500, 'Somethng went wrong, running the stock analysis')  
    return analysis

@app.route('/analyze-text', methods=['POST'])
def analyzeTextHandler():
    data = request.get_json()
    if 'text' not in data or not data['text']:
        abort(400, 'No text provided to analyze')
    analysis = analyzeText(data['text'])
    return analysis


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="0.0.0.0")