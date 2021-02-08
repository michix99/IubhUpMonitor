# A class to store all available runtime data on a website


class Website:
    def __init__(self, name="", url=""):
        self.name = name
        self.url = url
        self.availability = []
