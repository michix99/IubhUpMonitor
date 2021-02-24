import requests
import time
import os
import monitor
import statistics


# Monitor class
#
# Upon starts, loads sites.csv (pages we want to monitor)
# and sanity_checks.csv (pages we use to verify that we are online). Then used load_settings() to run and parse
# our settings.csv which contains import parameters for the running of the monitor
class Monitor:
    def __init__(self):
        print("Initializing Monitor")
        filepath = os.path.join(os.path.dirname(__file__), "config", "sanity_checks.csv")
        self.online_checks = self.load_sites(filepath)
        filepath = os.path.join(os.path.dirname(__file__), "config", "sites.csv")
        self.websites = self.load_sites(filepath)
        for site in self.websites:
            self.load_existing_data(site)
        self.config={}
        self.load_settings()

    # load settings from disc
    def load_settings(self):
        filepath = os.path.join(os.path.dirname(__file__), "config", "settings.csv")
        self.config["sleep_time"] = 60  # Use settings.csv to edit, this is just a default
        self.config["small_sleep"] = 1  # Use settings.csv to edit, this is just a default
        self.config["log_interval"] = 15  # Use settings.csv to edit, this is just a default
        self.config["small_logs"] = True  # Use settings.csv to edit, this is just a default
        self.config["max_timeout"] = 30  # Use settings.csv to edit, this is just a default
        try:
            with open(filepath) as file:
                for line in file:
                    if len(line.split(";")) > 1:
                        attr = line.split(";")[0]
                        value = int(line.split(";")[1])
                        if attr == "sleep_time":
                            self.config["sleep_time"] = value
                        if attr == "small_sleep":
                            self.config["small_sleep"] = value
                        if attr == "log_interval":
                            self.config["log_interval"] = value
                        if attr == "small_logs":
                            self.config["small_logs"] = bool(value)
                        if attr == "max_timeout":
                            self.config["max_timeout"] = value
        except FileNotFoundError:
            print("settings.csv not found, loading default settings")

    # Reads the local file at "path" and creates a list of website objects out of it
    @staticmethod
    def load_sites(path):
        site_list = []
        try:
            with open(path) as file:
                for line in file:
                    if line.startswith("#"):
                        continue
                    try:
                        w = monitor.Website(line.split(";")[0], line.split(";")[1])
                        site_list.append(w)
                    except IndexError:
                        print("List index out of range: " + line)
        except FileNotFoundError:
            print("File not found: " + path)
        return site_list

    # Check if we already have data on a website and if so append it to our new website object
    @staticmethod
    def load_existing_data(website, suffix=""):
        try:
            filename = website.name + suffix + ".json"
            filepath = os.path.join(os.path.dirname(__file__), "data", filename)
            with open(filepath, "r") as file:
                site = monitor.read_json(file)
                website.availability = site.availability
                website.latency = site.latency
                print("Loaded existing data for " + website.name)
        except FileNotFoundError:
            print("Could not find existing data for " + website.name)

    # Check pages that are typically available to make sure we are actually online
    def are_we_online(self):
        for check_site in self.online_checks:
            if self.check_availability(check_site, save=False, log=False) == "200":
                return True
        return False

    # Check if Website object is available and returns status as string
    #   save: Should the data be saved locally?
    #   log: Should the information be logged in the console? (Will not create linebreak until done)
    #
    #   Possible return values:
    #   -HTML Status code (200 = Okay, 503 = Service Unavailable etc.)
    #   -"999" in case of potential timeouts or other request errors
    def check_availability(self, website, save=True, log=True):
        status_code = "999"  # Pre initialize in case of timeout
        log = log if self.config["small_logs"] else False  # check if settings prohibit logging
        if log:
            print(website.name + ": ", end="", flush=True)
        try:
            latency = time.time() * 1000
            request = requests.get(website.url, timeout=self.config["max_timeout"])
            latency = int(time.time() * 1000 - latency)
            status_code = str(request.status_code)
        except requests.exceptions.RequestException:
            latency = -999
            pass
        if log:
            print(status_code + f" ({latency}ms)", end="", flush=True)
        if save:
            up = 1 if status_code == "200" else 0
            website.availability.append((int(time.time()), up))
            if latency != -999:
                website.latency.append((int(time.time()), latency))
            monitor.create_json(website)
            print(";", end=" ", flush=True)
        return status_code

    # Prints a big status update with the average
    # availability of the site over every data point
    def print_big_status(self):
        print("")
        print("===============================STATUS UPDATE===============================")
        for site in self.websites:
            avail_text = "\tNO DATA"
            lat_text = "\tNO DATA"
            if site.availability and site.latency:
                avg_lat = int(statistics.mean([data[1] for data in site.latency]))
                avg_up = statistics.mean([data[1] for data in site.availability])
                avail_text = str("%.2f" % avg_up)
                lat_text = str("%.0f" % avg_lat)
            print(
                f"{site.name:10}\t  avg.avail: {avail_text}\tavg.lat: {lat_text:>5}ms (Data: {len(site.availability)})")
        print("===========================================================================")

    # Checks all the sites in websites for their availability until manually exited
    # Prints a big status every log_interval checks and small status updates in between
    def run_monitor(self):
        print("Starting Monitoring")
        log_timer = 0  # Just counting
        while True:
            if log_timer % self.config["log_interval"] == 0 and self.config["log_interval"] != -1:
                self.print_big_status()
            log_timer += 1
            if self.are_we_online():
                for site in self.websites:
                    self.check_availability(site, log=True)
                    time.sleep(self.config["small_sleep"])
            else:
                print("NO INTERNET CONNECTION AVAILABLE", flush=True)
            timer = 0
            while timer < self.config["sleep_time"]:
                if self.config["small_logs"]:
                    print(".", end="", flush=True)  # Prints a dot every second while waiting
                time.sleep(1)
                timer += 1
            print("")
