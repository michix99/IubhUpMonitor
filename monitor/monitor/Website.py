# A class to store all available runtime data on a website
#

class Website:
    def __init__(self, name="", url=""):
        self.name = name
        self.url = url
        self.availability = []

    # Make sure our data is in order and containing valid values only
    def validate_data(self):
        old_date = 0
        for data in self.availability:
            if int(data[0]) > old_date:
                old_date = int(data[0])
            else:
                return False
            if 1 >= float(data[1]) >= 0:
                return True
            else:
                return False
