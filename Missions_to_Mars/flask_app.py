import json
from flask import Flask

app = Flask(__name__)

def read_data_json():
    with open('data.json') as json_file:
        data = json.load(json_file)
    return data

@app.route("/scrape")
def get_scrape_data():
    return f"<p>{str(read_data_json())}</p>"
