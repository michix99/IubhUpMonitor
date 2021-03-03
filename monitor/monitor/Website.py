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

    # Returns the averaged data between the utc_begin and utc_end moment of a given dataset
    # If extract=True will only return data within that timeframe
    # time_frame tells the function how many seconds should be compressed to a single datapoint
    @staticmethod
    def average_data(dataset, extract=False, utc_begin=0, utc_end=0, time_frame=0):
        if not dataset:
            return dataset
        if utc_end == 0:
            utc_end = time.time()  # If no end value is given, the current time is set as end value
        final_data = [dataset[0]]
        time_frame_data = []
        for data in dataset[1:]:
            data_utc = int(data[0])
            if not utc_begin < data_utc < utc_end:  # Check if data is in time we want to average
                if not extract:
                    final_data.append(data)  # If extract is false also append data outside our time frame
                continue
            if not time_frame_data:  # If the data of this time_frame is empty, use this as first node
                time_frame_data.append(data)
                continue
            if data_utc > int(time_frame_data[0][0]) + time_frame:  # Are we over our time_frame
                final_data.append((time_frame_data[-1][0], statistics.mean([i[1] for i in time_frame_data])))
                time_frame_data.clear()
            time_frame_data.append(data)
        if time_frame_data:
            final_data.append((time_frame_data[-1][0], statistics.mean([i[1] for i in time_frame_data])))
        return final_data

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
