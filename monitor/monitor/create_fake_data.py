import Website
import random
import time
import matplotlib.pyplot as plt
from Utils import create_json


def create_fake_data(website):
    # create fake data as specified by the following variables
    days_to_simulate = 1
    check_interval = 60  # in seconds
    avg_uptime = 0.9
    timestamp = int(time.time())  # not bothering with milliseconds
    timestamp -= days_to_simulate * 24 * 60 * 60  # roll back the time given amount of days
    while timestamp < time.time():
        up = 1 if random.uniform(0, 1) < avg_uptime else 0
        website.availability.append((timestamp, up))
        timestamp += check_interval


def plot_data(website):
    x_data = [data[0] for data in website.availability]
    y_data = [data[1] for data in website.availability]
    plt.plot(x_data, y_data)
    plt.show()


# Create a dummy website, fill it with random data and save it
myCampus = Website.Website("myCampus", "https://mycampus.iubh.de/")
create_fake_data(myCampus)
create_json(myCampus)
