import os

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import monitor_class
import json
import threading
import time


class Data(Resource):
    def __init__(self, website):
        self.website = website

    def get(self):
        try:
            filename = self.website.name + "-rest.json"
            filepath = os.path.join(os.path.dirname(__file__), "data", filename)
            with open(filepath, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print("Server could not open data for " + self.website.name)

    def __name__(self):
        return self.website.name


app = Flask(__name__)
api = Api(app)
m = monitor_class.Monitor()
api.add_resource(Data, "/data")

app.run()
m.run_monitor()
