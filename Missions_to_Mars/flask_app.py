import json
import pymongo
from flask import Flask, render_template, redirect, url_for
from jinja2 import Environment, PackageLoader, select_autoescape
from scrape_mars import scrape

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
    # Read the old scraping data from the json file
    old_data = read_data_json()

    # Use this as the pointer for replacing the document
    old_data_pointer = {
        "jpl_mars_space_images": old_data["jpl_mars_space_images"]
    }

    # Scrape web page and write the new data to data.json
    scrape()
    new_data = read_data_json()
    print(f"New web scraping data = {new_data}")

    # Insert the data into MongoDB
    result = data_collection.replace_one(old_data_pointer, new_data)
    print(f"Replaced old data = {old_data_pointer}")
    print(f"New data insertion id = {result}")
    return redirect(url_for('index'))

@app.route("/")
def index():
    # Read data from MongoDB
    data = data_collection.find_one()
    return render_template('index.html', data=data)
