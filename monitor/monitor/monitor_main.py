import requests
import monitor
import time

# The pages we use to make sure we are online
sanity_checks = [monitor.Website("Google", "https://www.google.com"),
                 monitor.Website("Amazon", "https://www.amazon.de/"),
                 monitor.Website("Facebook", "https://www.facebook.com")]

# The pages we intend to monitor
websites = [monitor.Website("myCampus", "https://mycampus.iubh.de/"),
            monitor.Website("webreader", "https://iubh.webreader.io/"),
            monitor.Website("BrainYoo", "https://brainyoo-webversion.iubh-fernstudium.de/"),
            monitor.Website("Care-FS", "https://care-fs.iubh.de/")]


# Check pages that are typically available to make sure the problem is not on our side
def are_we_online():
    for check_site in sanity_checks:
        if check_availability(check_site, save=False, log=False) == "200":
            return True
    return False


# Check if we already have data and if so append it to our new objects
def load_existing_data(website):
    try:
        with open(site.name + ".json", "r") as file:
            site.availability = monitor.read_json(file).availability
            print("Loaded existing data for " + site.name)
    except FileNotFoundError:
        print("Could not find existing data for " + site.name)


# Check if website is available and returns status as string
#   save: Should the data be saved locally?
#   log: Should the information be logged in the console? (Will not create linebreaks but tab at end!)
#
#   Possible return values:
#   -HTML Status code (200 = Okay, 503 = Service Unavailable etc.)
#   -"-999" in case of potential timeouts or other request errors

def check_availability(website, save=True, log=True):
    status_code = "-999"
    try:
        request = requests.get(website.url, timeout=30)
        status_code = str(request.status_code)
    except requests.exceptions.RequestException:
        pass
    if log:
        print(website.name + " Status: " + status_code + "; ", end="\t")
    if save:
        up = 1 if status_code == "200" else 0
        website.availability.append((int(time.time()), up))
        monitor.create_json(website)
    return status_code


# Prints a big status update with the average
# availability of the site over every data point
def print_big_status():
    print("")
    print("===============================STATUS UPDATE===============================")
    for status_site in websites:
        avg_up = 0
        for d in status_site.availability:
            avg_up += d[1]
        avg_up /= len(status_site.availability)
        print("Average availability of " + status_site.name + ":\t" + str("%.3f" % avg_up) + " (Data size: " +
              str(len(status_site.availability)) + ")")
    print("===========================================================================")


# MAIN BODY BEGINS HERE
# First tries to load existing data if available
# Then checks all the sites in websites for their availability until manually exited
# Prints a big status every log_interval checks and small status updates in between
sleep_time = 60  # How to long to wait between each round of checks
small_sleep = 1  # How long to wait between each single page
log_interval = 15  # How often does a big status get printed
log_timer = 0  # Just counting
for site in websites:
    load_existing_data(site)
while True:
    print("CHECKING: ")
    if are_we_online():
        for site in websites:
            check_availability(site, log=True)
            time.sleep(small_sleep)
        if log_timer % log_interval == 0:
            print_big_status()
        log_timer += 1
    else:
        print("NO INTERNET CONNECTION AVAILABLE", end="")
    timer = 0
    while timer < sleep_time:
        print(".", end="")
        time.sleep(1)
        timer += 1
    print("")
