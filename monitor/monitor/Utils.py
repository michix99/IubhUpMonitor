# A class to automate the creation of appropriately structured .json files
import time

import matplotlib.pyplot as plt
import monitor
import json
import os


# create a json file from a given website and (for now) save it locally
# readable should only be True for debugging the json manually
# The suffix will be appended to the json (for saving compressed files)
def create_json(website, readable=False, suffix=""):
    zipped = {"website": [], "status": [], "data": []}
    zipped["website"].append({
        "name": website.name,
        "url": website.url
    })
    filename = website.name + suffix + ".json"
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    zipped["data"] = website.get_zip()
    zipped["status"] = website.get_status()
    with open(filepath, "w") as file:
        if readable:
            json.dump(zipped, file, indent=4)
        else:
            json.dump(zipped, file)


# Create a small status json of a given website with the core stats
def create_status_json(website):
    data = {"website": [], "status": []}
    data["website"].append({
        "name": website.name,
        "url": website.url
    })
    filename = website.name + "-status" + ".json"
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    data["status"] = website.get_status()
    with open(filepath, "w") as file:
        json.dump(data, file)


# read a given zipped json_file and extract the data points in it to return a website object
def read_json(json_file):
    try:
        zipped = json.load(json_file)
        site = monitor.Website(zipped["website"][0]["name"], zipped["website"][0]["url"])
        for utc in zipped["data"]:
            if zipped["data"][utc][0] != "-1":
                site.availability.append((utc, zipped["data"][utc][0]))
            if zipped["data"][utc][1] != "-1":
                site.latency.append((utc, zipped["data"][utc][1]))

    except json.decoder.JSONDecodeError:
        print("ERROR: Malformed json file")
        return
    except KeyError:
        print("ERROR: Could not find key in json_file")
        return
    return site


# Currently just used for debugging to verify we compress and average our data correctly
def plot_data(website, suffix=""):
    fig, ax1 = plt.subplots()
    x_data = [(int(data[0]) - int(time.time())) / 60 for data in website.availability]
    y_data = [data[1] for data in website.availability]
    color = 'tab:orange'
    ax1.set_xlabel('minutes ago)')
    ax1.set_ylabel('availability', color=color)
    ax1.plot(x_data, y_data, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    x_data = [(int(data[0]) - int(time.time())) / 60 for data in website.latency]
    y_data = [data[1] for data in website.latency]
    color = 'tab:blue'
    ax2.set_ylabel('latency', color=color)
    ax2.plot(x_data, y_data, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title(website.name + suffix + " Data Points :" + str(len(website.availability)))
    plt.show()


def get_seconds(seconds=0, minutes=0, hours=0, days=0):
    return seconds + minutes * 60 + hours * 3600 + days * 3600 * 24


def get_past_utc(seconds):
    return int(time.time() - seconds)


# Availability and Latency will be compiled together as good as possible to reduce file size
# If they share a UTC time code, wrap them together
# Returns it as a dictionary ready for json saving
def get_zip(availability, latency):
    data = {}
    for av in availability:
        data[av[0]] = (av[1], -1)
    for lat in latency:
        if lat[0] in data:
            data[lat[0]] = (data[lat[0]][0], lat[1])
        else:
            data[lat[0]] = (-1, lat[1])
    return data
