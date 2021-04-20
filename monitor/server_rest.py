import os
import json
from flask import Flask, abort
from utils import load_sites


app = Flask(__name__)
websites = []

def setup_app(app):
    global websites
    sites_path = os.path.join(os.path.dirname(__file__), "config", "sites.csv")
    websites = load_sites(sites_path)

@app.route("/sites")
def sites():
    global websites
    data = {
        "sites": []
    }
    for site in websites:
        data["sites"].append(site.name)
    return data

@app.route("/data")
def all_data():
    global websites
    data = {
        "sites": []
    }
    for site in websites:
        try:
            file_path = "data/%s-rest.json" % site.name
            with open(file_path, "r") as file:
                single_data = json.load(file)
                formated = single_data["website"]
                formated["data"] = single_data["data"]
                data["sites"].append(formated)
        except FileNotFoundError:
            abort(404)
    return data

@app.route("/data/<website>")
def single_data(website):
    try:
        file_path = "data/%s-rest.json" % website
        with open(file_path, "r") as file:
            data = json.load(file)
            del data["status"]
            return data
    except FileNotFoundError:
        abort(404)

@app.route("/status")
def all_status():
    global websites
    data = {
        "sites": []
    }
    for site in websites:
        try:
            file_path = "data/%s-rest.json" % site.name
            with open(file_path, "r") as file:
                single_data = json.load(file)
                formated = single_data["website"]
                formated["status"] = single_data["status"]
                data["sites"].append(formated)
        except FileNotFoundError:
            abort(404)
    return data

@app.route("/status/<website>")
def single_status(website):
    try:
        file_path = "data/%s-rest.json" % website
        with open(file_path, "r") as file:
            data = json.load(file)
            del data["data"]
            return data
    except FileNotFoundError:
        abort(404)

setup_app(app)
app.run()
