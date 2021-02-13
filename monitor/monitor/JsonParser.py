# A class to automate the creation of appropriately structured .json files

import monitor
import json


# create a json file from a given website and (for now) save it locally
def create_json(website, readable=False):
    data = {"website": [], "availability": []}
    data["website"].append({
        "name": website.name,
        "url": website.url
    })
    filename = website.name + ".json"
    for uptime in website.availability:
        data["availability"].append({uptime[0]: uptime[1]})
    with open("data/" + filename, "w") as file:
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
