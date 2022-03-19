import json
import pymongo
from flask import Flask, render_template
from jinja2 import Environment, PackageLoader, select_autoescape

# Initialize Jinja environment
env = Environment(
    loader=PackageLoader("flask_app"),
    autoescape=select_autoescape()
)

# Initialize Flask app
app = Flask(__name__)

# Initialize MongoDB
connection_url = "mongodb+srv://admin:admin@cluster0.2g1sk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_url)
web_scrape_db = client["web_scrape_db"]  # Create database
data_collection = web_scrape_db["data"]  # Create collection

def read_data_json():
    """
    Reads the web scraping data from the data.json file in Missions_to_Mars.
    This file is written by the scrape_mars.py file.
    :return:
    """
    with open('data.json') as json_file:
        data = json.load(json_file)
    return data

@app.route("/scrape")
def get_scrape_data():
    # data = read_data_json()
    # result = data_collection.insert_one(data)
    return f"<p>hey there</p>"

@app.route("/")
def test():
    # Read data from MongoDB
    data = data_collection.find_one()
    return render_template('index.html', data=data)
