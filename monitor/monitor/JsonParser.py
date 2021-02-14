# A class to automate the creation of appropriately structured .json files
import matplotlib.pyplot as plt
import monitor
import json
import os
import time


# create a json file from a given website and (for now) save it locally
def create_json(website, readable=False, suffix=""):
    data = {"website": [], "availability": []}
    data["website"].append({
        "name": website.name,
        "url": website.url
    })
    filename = website.name + suffix + ".json"
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    for uptime in website.availability:
        data["availability"].append({uptime[0]: uptime[1]})
    with open(filepath, "w") as file:
        if readable:
            json.dump(data, file, indent=4)
        else:
            json.dump(data, file)


# read a given json file and return a website object
def read_json(json_file):
    try:
        data = json.load(json_file)
        site = monitor.Website(data["website"][0]["name"], data["website"][0]["url"])
        for d in data["availability"]:
            for key in d:
                site.availability.append((key, d[key]))
    except json.decoder.JSONDecodeError:
        print("ERROR: Malformed json file")
        return
    except KeyError:
        print("ERROR: Could not find key in json_file")
        return
    return site


def plot_data(website, suffix=""):
    x_data = [int(data[0]) for data in website.availability]
    y_data = [data[1] for data in website.availability]
    plt.plot(x_data, y_data)
    plt.title(website.name + suffix + " Data Points :" + str(len(website.availability)))
    plt.show()


def get_average(data_tuples):
    avg = 0
    for d in data_tuples:
        avg += d[1]
    avg = avg / len(data_tuples)
    return data_tuples[-1][0], avg


def average_data(website, start=0, end=0, seconds=0, minutes=0, hours=0, days=0):
    if end == 0:
        end = time.time()
    time_slot = seconds + minutes * 60 + hours * 60 * 60 + days * 24 * 60 * 60
    print("Averaging " + website.name + " values over " + str(time_slot) + " seconds, current size: " + str(
        len(website.availability)))
    avg_data = []
    temp_data = []
    for data in website.availability:
        timestamp = int(data[0])
        if timestamp < start or timestamp > end:
            avg_data.append(data)
            continue
        if len(avg_data) == 0:
            avg_data.append(data)
        if len(temp_data) == 0:
            temp_data.append(data)
            continue
        if timestamp > int(temp_data[0][0]) + time_slot:
            avg_data.append(get_average(temp_data))
            temp_data.clear()
        temp_data.append(data)
    website.availability = avg_data
    print("Averaged " + website.name + "values new size: " + str(
        len(website.availability)))


def compress_data(website):
    avl = website.availability
    print("Compressing Data of " + website.name + ",  old size: " + str(len(avl)))
    compressed = []
    if len(avl) < 3:
        print("Too small to compress")
        return
    compressed.append(avl[0])
    old_avail = avl[0]
    for data in avl:
        if data[1] != compressed[-1][1]:
            print("Current data: {0} Latest compressed: {1} ".format(data[1], compressed[-1][1]))
            print("Old data: {0}".format(old_avail[1]))
            if compressed[-1] != old_avail:
                compressed.append(old_avail)
            compressed.append(data)
        old_avail = data
    if compressed[-1] == avl[-1]:
        pass
    else:
        compressed.append(avl[-1])
    website.availability = compressed
    print("Compressed Data, new size: " + str(len(website.availability)))


def compress_plot_save(websites):
    for site in websites:
        plot_data(site)
        average_data(site, minutes=15)
        monitor.create_json(site, readable=False, suffix="-averaged")
        plot_data(site, " Averaged")
        compress_data(site)
        monitor.create_json(site, readable=False, suffix="-averagedcompressed")
        plot_data(site, " Averaged + Compressed")
