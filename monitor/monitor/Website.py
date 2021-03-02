import time
import statistics

# A class to store all available runtime data on a website
# availability: tuple to store our main data, format: (UTC-Timestamp,availability)
# availability will be a number between 0 and 1 and the timestamp is the average availability from the
# previous timestamp to this one (in case of raw data it will only be 1 or 0)
# latency: tuple to store the sites latency data, format: (UTC-Timestamp,latency)
# latency will be given as a millisecond value
from monitor.Utils import get_past_utc, get_seconds


class Website:
    def __init__(self, name="", url=""):
        self.name = name
        self.url = url
        self.availability = []
        self.latency = []

    # Returns the averaged data between the start and end moment (in UTC) of a given dataset
    # If extract=True will only return data within that timeframe
    # seconds, minutes, hours, and days regulates how big the timeframe is for a single data point
    # e.g. if the setting is one hour, the algorithm will take every datapoint within one hour and average it
    # to a single data point with the time of the _last_ data point in that time frame
    @staticmethod
    def average_data(dataset, extract=False, begin=0, end=0, seconds=0, minutes=0, hours=0, days=0):
        if end == 0:
            end = time.time()  # If no end value is given, the current time is set as end value
        time_frame = seconds + minutes * 60 + hours * 360 + days * 86.400  # How many seconds is each data point?
        avg_data = []  # Our final result
        temp_data = []  # This will hold the temporary data of a time_frame before avg. it and adding it to avg_data
        for data in dataset:
            timestamp = int(data[0])
            if timestamp < begin or timestamp > end:  # Check if data is in time we want to average
                if not extract:  # If extract is true, disregard outside of timeframe
                    avg_data.append(data)  # If extract is false, append it not averaged
                continue
            if len(avg_data) == 0:  # If our dataset is empty, use this as a first node
                avg_data.append(data)
            if len(temp_data) == 0:  # If the data of this timeslot is empty, use this as first node
                temp_data.append(data)
                continue
            if timestamp > int(temp_data[0][0]) + time_frame:  # Are we over our timeframe
                avg_data.append((temp_data[-1][0], statistics.mean([i[1] for i in temp_data])))
                temp_data.clear()
            temp_data.append(data)
        if len(temp_data) > 0:
            avg_data.append((temp_data[-1][0], statistics.mean([i[1] for i in temp_data])))
        return avg_data

    # compresses the availability data of the website without loss of detail, merges successive data points
    # with the same value to a single datapoint with the timestamp of the last datapoint
    def compress_data(self):
        avl = self.availability
        compressed = []
        if len(avl) < 3:
            return
        compressed.append(avl[0])
        old_avail = avl[0]
        for data in avl:
            if data[1] == -1:
                continue
            if data[1] != compressed[-1][1]:
                if compressed[-1] != old_avail:
                    compressed.append(old_avail)
                compressed.append(data)
            old_avail = data
        if compressed[-1] == avl[-1]:
            pass
        else:
            compressed.append(avl[-1])
        self.availability = compressed

    # Returns the current website status as a dictionary for storing as json
    # "Online" = The status over the last 15 minutes
    # "Online" = "RED" : 90%> of data points not available
    # "Online" = "YELLOW" : some times not available
    # "Online" = "GREEN" : Page online 100%
    # "Latency" = The average latency over the last 15 minutes
    # "Availability" = Lifetime average availability
    # "LastOff" = UTC timestamp of the last offline occurrence (-1 if no recorded offline occurrence)
    def get_status(self):
        time_window = get_past_utc(get_seconds(minutes=15))
        try:
            online = statistics.mean(
                d[1] for d in self.average_data(self.availability, begin=time_window, extract=True))
            lat = int(statistics.mean(
                d[1] for d in self.average_data(self.latency, begin=time_window, extract=True, minutes=1)))
            availability = statistics.mean(d[1] for d in self.availability)
        except statistics.StatisticsError:
            # We have no Data available right now
            online = 1
            lat = "--"
            availability = 1
        try:
            last_off = max([int(d[0]) for d in self.average_data(self.availability, minutes=5) if d[1] < 1])
        except ValueError:
            last_off = -1
        if online == 1:
            online = "GREEN"
        elif online < 0.5:
            online = "RED  "
        else:
            online = "YELLOW"
        status = {"Online": online, "Latency": lat, "Availability": availability, "LastOff": last_off}
        return status
