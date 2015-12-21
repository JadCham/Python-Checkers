class Message:

    def __init__(self, ffrom, to, data):
        self.ffrom = ffrom
        self.to = to
        self.data = data

    def getdest(self):
        return self.to

    def getfrom(self):
        return self.ffrom

    def getdata(self):
        return self.data
