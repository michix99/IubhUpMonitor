import requests
import monitor
import time


class Monitor:

    def __init__(self):

        # The pages we use to make sure we are online
        self.sanity_checks = self.load_sites("config/sanity_checks.csv")
        # The pages we intend to monitor
        self.websites = self.load_sites("config/sites.csv")
        for site in self.websites:
            self.load_existing_data(site)

        self.sleep_time = 60  # Use settings.csv to edit, this is just a default
        self.small_sleep = 1  # Use settings.csv to edit, this is just a default
        self.log_interval = 15  # Use settings.csv to edit, this is just a default
        self.small_logs = True  # Use settings.csv to edit, this is just a default
        self.load_settings()

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

    # Check if we already have data and if so append it to our new objects
    @staticmethod
    def load_existing_data(website):
        try:
            with open("data/" + website.name + ".json", "r") as file:
                website.availability = monitor.read_json(file).availability
                if not website.validate_data():
                    print("Error in data of " + website.name)
                print("Loaded existing data for " + website.name)
        except FileNotFoundError:
            print("Could not find existing data for " + website.name)

    # Check pages that are typically available to make sure the problem is not on our side
    def are_we_online(self):
        for check_site in self.sanity_checks:
            if self.check_availability(check_site, save=False, log=False) == "200":
                return True
        return False

    # Check if website is available and returns status as string
    #   save: Should the data be saved locally?
    #   log: Should the information be logged in the console? (Will not create linebreaks but tab at end!)
    #
    #   Possible return values:
    #   -HTML Status code (200 = Okay, 503 = Service Unavailable etc.)
    #   -"-999" in case of potential timeouts or other request errors
    def check_availability(self, website, save=True, log=True):
        status_code = "-999"  # Pre initialize in case of timeout
        latency = -999  # Pre initialize in case of timeout
        log = log if self.small_logs else False  # check if settings prohibit logging
        if log:
            print(website.name + ": ", end="")
        try:
            latency = time.time() * 1000
            request = requests.get(website.url, timeout=30)
            latency = int(time.time() * 1000 - latency)
            status_code = str(request.status_code)
        except requests.exceptions.RequestException:
            pass
        latency_string = str(latency) if status_code != "-999" else "-"
        if log:
            print(status_code + "(" + latency_string + "ms); ", end="\t")
        if save:
            up = 1 if status_code == "200" else 0
            website.availability.append((int(time.time()), up))
            monitor.create_json(website)
        return status_code

    # Prints a big status update with the average
    # availability of the site over every data point
    def print_big_status(self):
        print("")
        print("===============================STATUS UPDATE===============================")
        for status_site in self.websites:
            avg_up = 0
            for d in status_site.availability:
                avg_up += d[1]
            if len(status_site.availability) > 0:
                status_text = str("%.3f" % (avg_up / len(status_site.availability)))
            else:
                status_text = "\tNO DATA AVAILABLE"
            print("Average availability of " + status_site.name + ":\t" + status_text + " (Data size: " +
                  str(len(status_site.availability)) + ")")
        print("===========================================================================")

    # Checks all the sites in websites for their availability until manually exited
    # Prints a big status every log_interval checks and small status updates in between
    def run_monitor(self):
        log_timer = 0  # Just counting
        while True:
            if log_timer % self.log_interval == 0 and self.log_interval != -1:
                self.print_big_status()
            log_timer += 1
            if self.are_we_online():
                for site in self.websites:
                    self.check_availability(site, log=True)
                    time.sleep(self.small_sleep)
            else:
                print("NO INTERNET CONNECTION AVAILABLE", end="")
            timer = 0
            while timer < self.sleep_time:
                if self.small_logs:
                    print(".", end="")  # Prints a dot every second while waiting
                time.sleep(1)
                timer += 1
            print("")

    def load_settings(self):
        try:
            with open("config/settings.csv") as file:
                for line in file:
                    if len(line.split(";")) > 1:
                        attr = line.split(";")[0]
                        value = int(line.split(";")[1])
                        if attr == "sleep_time":
                            self.sleep_time = value
                        if attr == "small_sleep":
                            self.small_sleep = value
                        if attr == "log_interval":
                            self.log_interval = value
                        if attr == "small_logs":
                            self.small_logs = bool(value)
        except FileNotFoundError:
            print("settings.csv not found, loading default settings")


m = Monitor()
m.run_monitor()
