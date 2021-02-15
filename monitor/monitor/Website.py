import time
import statistics


# A class to store all available runtime data on a website
# availability: tuple to store our main data, format: (UTC-Timestamp,availability)
# availability will be a number between 0 and 1 and the timestamp is the average availability from the
# previous timestamp to this one (in case of raw data it will only be 1 or 0)

class Website:
    def __init__(self, name="", url=""):
        self.name = name
        self.url = url
        self.availability = []

    # Average the data between the start and end moment (in UTC)
    # seconds, minutes, hours, and days regulates how big the timeframe is for a single data point
    # e.g. if the setting is one hour, the algorithm will take every datapoint within one hour and average it
    # to a single data point with the time of the _last_ data point in that time frame
    def average_data(self, start=0, end=0, seconds=0, minutes=0, hours=0, days=0):
        if end == 0:
            end = time.time()
        time_frame = seconds + minutes * 60 + hours * 60 * 60 + days * 24 * 60 * 60
        print("Averaging " + self.name + " values over " + str(time_frame) + " seconds, current size: " + str(
            len(self.availability)))
        avg_data = []
        temp_data = []
        for data in self.availability:
            timestamp = int(data[0])
            if timestamp < start or timestamp > end:
                avg_data.append(data)
                continue
            if len(avg_data) == 0:
                avg_data.append(data)
            if len(temp_data) == 0:
                temp_data.append(data)
                continue
            if timestamp > int(temp_data[0][0]) + time_frame:
                avg_data.append((temp_data[-1][0], statistics.mean([i[1] for i in temp_data])))
                temp_data.clear()
            temp_data.append(data)
        self.availability = avg_data
        print("Averaged " + self.name + "values new size: " + str(
            len(self.availability)))

    # compresses the data of the website without loss of detail, merges successive datapoints with the same value
    # to a single datapoint with the timestamp of the last datapoint
    def compress_data(self):
        avl = self.availability
        print("Compressing Data of " + self.name + ",  old size: " + str(len(avl)))
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
        self.availability = compressed
        print("Compressed Data, new size: " + str(len(self.availability)))
