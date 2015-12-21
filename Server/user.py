class User:

    # Constructor
    def __init__(self, name, username, password, score, ip):
        self._name = name
        self._username = username
        self._password = password
        self._online = True
        self._score = score
        self._ip = ip

    # Setters
    def setname(self, name):
        self._name = name

    def setusername(self, username):
        self._username = username

    def setpassword(self, password):
        self._password = password

    def updatescore(self, increment):
        self._score += increment

    def setonline(self):
        self._online = True

    def setip(self, ip):
        self._ip = ip

    # Getters
    def getname(self):
        return self._name

    def getusername(self):
        return self._username

    def getpassword(self):
        return self._password

    def getscore(self):
        return self._score

    def isonline(self):
        return self._online

    def getip(self):
        return self._ip
