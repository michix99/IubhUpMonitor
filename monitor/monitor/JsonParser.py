# A class to automate the creation of appropriately structured .json files
import matplotlib.pyplot as plt
import monitor
import json
import os


# create a json file from a given website and (for now) save it locally
# readable should only be True for debugging the json manually
# The suffix will be appended to the json (for saving compressed files)
def create_json(website, readable=False, suffix=""):
    data = {"website": [], "availability": [], "latency": []}
    data["website"].append({
        "name": website.name,
        "url": website.url
    })
    filename = website.name + suffix + ".json"
    filepath = os.path.join(os.path.dirname(__file__), "data", filename)
    for uptime in website.availability:
        data["availability"].append({uptime[0]: uptime[1]})
    for latency in website.latency:
        data["latency"].append({latency[0]: latency[1]})
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
        for d in data["latency"]:
            for key in d:
                site.latency.append((key, d[key]))
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
    x_data = [int(data[0]) for data in website.availability]
    y_data = [data[1] for data in website.availability]
    color = 'tab:orange'
    ax1.set_xlabel('time (UTC)')
    ax1.set_ylabel('availability', color=color)
    ax1.plot(x_data, y_data, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    x_data = [int(data[0]) for data in website.latency]
    y_data = [data[1] for data in website.latency]
    color = 'tab:blue'
    ax2.set_ylabel('latency', color=color)
    ax2.plot(x_data, y_data, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title(website.name + suffix + " Data Points :" + str(len(website.availability)))
    plt.show()


# Used for debugging to compress, plot and save every website in a given list
def compress_plot_save(websites):
    for site in websites:
        plot_data(site)
        site.availability = site.average_data(site.availability, minutes=15)
        monitor.create_json(site, readable=False, suffix="-averaged")
        plot_data(site, " Averaged")
        site.compress_data()
        monitor.create_json(site, readable=False, suffix="-averagedcompressed")
        plot_data(site, " Averaged + Compressed")
