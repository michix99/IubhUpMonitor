# A class to automate the creation of appropriately structured .json files
import time
import Website
import matplotlib.pyplot as plt
import json
import os


# Create the rest.json that will be shared, averages over months, weeks and days
def create_rest_json(website):

    site = Website.Website(website.name, website.url)
    month_ago = get_past_utc(get_sec(days=30))
    week_ago = get_past_utc(get_sec(days=7))
    day_ago = get_past_utc(get_sec(days=1))
    month_factor_lat = get_sec(days=1)
    month_factor_avl = get_sec(hours=3)
    week_factor_lat = get_sec(hours=3)
    week_factor_avl = get_sec(hours=1)
    day_factor_lat = get_sec(minutes=15)
    day_factor_avl = get_sec(minutes=5)
    avl = site.average_data(website.availability, utc_begin=month_ago, utc_end=week_ago, time_frame=month_factor_avl,
                            extract=True)
    avl.extend(site.average_data(website.availability, utc_begin=week_ago, utc_end=day_ago, time_frame=week_factor_avl,
                                 extract=True))
    avl.extend(site.average_data(website.availability, utc_begin=day_ago, time_frame=day_factor_avl,
                                 extract=True))
    lat = site.average_data(website.latency, utc_begin=month_ago, utc_end=week_ago, time_frame=month_factor_lat,
                            extract=True)
    lat.extend(site.average_data(website.latency, utc_begin=week_ago, utc_end=day_ago, time_frame=week_factor_lat,
                                 extract=True))
    lat.extend(site.average_data(website.latency, utc_begin=day_ago, time_frame=day_factor_lat,
                                 extract=True))
    site.availability = avl
    site.latency = lat
    site.compress_data()
    create_json(site, suffix="-rest")
    return site


# create a json file from a given website and save it locally
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
    zipped["data"] = get_zip(website.availability, website.latency)
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
        site = Website.Website(zipped["website"][0]["name"], zipped["website"][0]["url"])
        for utc in zipped["data"]:
            if zipped["data"][utc][0] != -1:
                site.availability.append((int(utc), zipped["data"][utc][0]))
            if zipped["data"][utc][1] != -1:
                site.latency.append((int(utc), zipped["data"][utc][1]))

    except json.decoder.JSONDecodeError:
        print("ERROR: Malformed json file")
        return
    except KeyError:
        print("ERROR: Could not find key in json_file")
        return
    return site


# Used for debugging to verify we compress and average our data correctly
def plot_data(website, suffix=""):
    fig, ax1 = plt.subplots()
    x_data = [(int(data[0]) - int(time.time())) / 60 for data in website.availability]
    y_data = [data[1] for data in website.availability]
    color = 'tab:orange'
    ax1.set_xlabel('minutes ago)')
    ax1.set_ylabel('availability', color=color)
    ax1.plot(x_data, y_data, color=color, marker="o")
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    x_data = [(int(data[0]) - int(time.time())) / 60 for data in website.latency]
    y_data = [data[1] for data in website.latency]
    color = 'tab:blue'
    ax2.set_ylabel('latency', color=color)
    ax2.plot(x_data, y_data, color=color, marker="o")
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title(website.name + suffix + " Data Points :" + str(len(website.availability)))
    plt.show()


def get_sec(seconds=0, minutes=0, hours=0, days=0):
    return seconds + minutes * 60 + hours * 3600 + days * 3600 * 24


def get_past_utc(seconds):
    return int(time.time() - seconds)


# Helper function to zip data in dictionaries
def dic_insert(dic, utc, av, lat):
    if utc in dic:
        if dic[utc][0] == -1:
            dic[utc] = (av, dic[utc][1])
        if dic[utc][1] == -1:
            dic[utc] = (dic[utc][0], lat)
    else:
        dic[utc] = (av, lat)


# Availability and Latency will be compiled together as good as possible to reduce file size
# If they share a UTC time code, wrap them together
# Returns it as a dictionary ready for json saving
def get_zip(availability, latency):
    data = {}
    av_copy = availability[:]
    lat_copy = latency[:]
    while len(av_copy) > 0 or len(lat_copy) > 0:
        av_time = av_copy[0][0] if len(av_copy) > 0 else lat_copy[0][0] + 1
        lat_time = lat_copy[0][0] if len(lat_copy) > 0 else av_copy[0][0] + 1
        if av_time < lat_time:
            item = av_copy.pop(0)
            dic_insert(data, av_time, item[1], -1)
        else:
            item = lat_copy.pop(0)
            dic_insert(data, lat_time, -1, item[1])
    return data
