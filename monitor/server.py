from flask import Flask, abort
import json


app = Flask(__name__)


@app.route("/BrainYoo/data")
def brainyoo_data():
    try:
        with open("data/BrainYoo-rest.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        abort(404)


@app.route("/BrainYoo/status")
def brainyoo_status():
    try:
        with open("data/BrainYoo-rest.json", "r") as file:
            data = json.load(file)
            del data["data"]
            return data
    except FileNotFoundError:
        abort(404)


@app.route("/myCampus/data")
def mycampus_data():
    try:
        with open("data/myCampus-rest.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        abort(404)


@app.route("/myCampus/status")
def mycampus_status():
    try:
        with open("data/myCampus-rest.json", "r") as file:
            data = json.load(file)
            del data["data"]
            return data
    except FileNotFoundError:
        abort(404)


@app.route("/Care-FS/data")
def carefs_data():
    try:
        with open("data/Care-FS-rest.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        abort(404)


@app.route("/Care-FS/status")
def carefs_status():
    try:
        with open("data/Care-FS-rest.json", "r") as file:
            data = json.load(file)
            del data["data"]
            return data
    except FileNotFoundError:
        abort(404)


@app.route("/webreader/data")
def webreader_data():
    try:
        with open("data/webreader-rest.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        abort(404)


@app.route("/webreader/status")
def webreader_status():
    try:
        with open("data/webreader-rest.json", "r") as file:
            data = json.load(file)
            del data["data"]
            return data
    except FileNotFoundError:
        abort(404)


app.run()
