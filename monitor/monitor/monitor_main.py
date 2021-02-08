import requests
import monitor
import time

websites = []
myCampus = monitor.Website("myCampus", "https://mycampus.iubh.de/")
webreader = monitor.Website("webreader", "https://iubh.webreader.io/")
brainyoo = monitor.Website("BrainYoo", "https://brainyoo-webversion.iubh-fernstudium.de/")
care = monitor.Website("Care", "https://care-fs.iubh.de/")
websites.append(myCampus)
websites.append(webreader)
websites.append(brainyoo)
websites.append(care)

sleep_time = 60
log_timer = 0
log_interval = 15

for site in websites:
    with open(site.name + ".json", "r") as file:
        site.availability = monitor.read_json(file).availability
    print("Starting monitoring of " + site.name)

while True:
    for site in websites:
        request = requests.get(site.url)
        up = 1 if request.status_code == 200 else 0
        site.availability.append((int(time.time()), up))
        status = str(up) if up == 1 else request.status_code
        print("Checking: " + site.name + " Status: " + status + "; ", end="")
        monitor.create_json(site)
        time.sleep(2)
    if log_timer % log_interval == 0:
        print("")
        print("===============================STATUS UPDATE===============================")
        print("Monitoring for " + str(log_timer) + " minutes")
        for site in websites:
            avg_up = 0
            for d in site.availability:
                avg_up += d[1]
            avg_up /= len(site.availability)
            print("Average Uptime of " + site.name + ": " + str(avg_up))
        print("===========================================================================")
    log_timer += 1
    timer = 0
    while timer < sleep_time:
        print(".", end="")
        time.sleep(1)
        timer += 1
    print("")
