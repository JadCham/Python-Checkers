import user
import datamanager

class RequestManager:

    def __init__(self, data, ip, port, clientserver):
        self.data = data
        self._ip = ip
        self._port = port
        self._server = clientserver
        self.datamgr = datamanager.DataManager("localhost", "liwaa", "p@ss0rd", "testDatabase")

    # Define the message's category before parsing
    def parsedata(self):
        if self.data.__contains__("msg:/"):
            return self.parsemsg()
        elif self.data.__contains__("afriend:/"):
            return self.parseaddfriend()
        elif self.data.__contains__("greq:/"):
            return self.parsegamerequest()
        elif self.data.__contains__("update:/"):
            return self.parseupdate()
        elif self.data.__contains__("auth:/"):
            return self.parseauth()
        elif self.data.__contains__("adduser:/"):
            return self.parseadduser()
        elif self.data.__contains__("ison:/"):
            return self.parseonline()
        elif self.data.__contains__("isoff:/"):
            return self.parseoffline()
        elif self.data.__contains__("accept:/"):
            return self.parseacceptfriendrequest()
        elif self.data.__contains__("reject:/"):
            return self.parserejectfriendrequest()
        elif self.data.__contains__("getprofile:/"):
            return self.parsegetprofile()
        else:
            print "Error ! Data has a wrong format --> %s" % self.data

    # Online checking
    def parseonline(self):
        suser = False
        username = ""
        for c in self.data:
            if suser:
                username += c
            if c == '/':
                suser = True
        self.data = ""
        # print "user %s is on" % username
        self.datamgr.setonline(username)
        return self.datamgr.getonlinefriends(username)

    def parseoffline(self):
        suser = False
        username = ""
        for c in self.data:
            if suser:
                username += c
            if c == '/':
                suser = True
        return ""
        self.data = ""
        print "%s is now offline" % username

    # Actual Parsing by category

    # Chat Request Parsing
    def parsemsg(self):
        to = ""
        ffrom = ""
        sfrom = False
        sto = False
        for c in self.data:
            if sto:
                to += c
            if c == '|':
                sto = True
                sfrom = False
            if sfrom:
                ffrom += c
            if c == '/':
                sfrom = True
        userip = "mip:/"
        userto = self.datamgr.getuserobject(to)
        userip += userto.getip()
        return userip

    # Add Friend
    def parseaddfriend(self):
        suser = False
        sfriend = False
        username = ""
        friend = ""
        for c in self.data:
            if sfriend:
                friend += c
            if c == '|':
                suser = False
                sfriend = True
            if suser:
                username += c
            if c == '/':
                suser = True
        self.data = ""
        return self.datamgr.addfriend(username, friend)

    def acceptfriendrequest(self):
        suser = False
        sfriend = False
        username = ""
        friend = ""
        for c in self.data:
            if sfriend:
                friend += c
            if c == '|':
                suser = False
                sfriend = True
            if suser:
                username += c
            if c == '/':
                suser = True
        self.data = ""
        return self.datamgr.acceptfriend(username, friend)

    #reject friend request
    def rejecttfriendrequest(self):
        suser = False
        sfriend = False
        username = ""
        friend = ""
        for c in self.data:
            if sfriend:
                friend += c
            if c == '|':
                suser = False
                sfriend = True
            if suser:
                username += c
            if c == '/':
                suser = True
        self.data = ""
        return self.datamgr.rejectfriend(username, friend)

    def parsegamerequest(self):
        to = ""
        ffrom = ""
        sfrom = False
        sto = False
        for c in self.data:
            if sto:
                to += c
            if c == '|':
                sto = True
                sfrom = False
            if sfrom:
                ffrom += c
            if c == '/':
                sfrom = True
        userip = "gip:/"
        userto = self.datamgr.getuserobject(to)
        userip += userto.getip()
        return userip

    #Get Profile Details
    def parsegetprofile(self):
        suser = False
        username = ""
        for c in self.data:
            if suser:
                username += c
            if c == '/':
                suser = True
        newuser = self.datamgr.getuserobject(username)
        response = "%s|%s|%s" % (newuser._name, newuser._username, newuser._score)
        return response

    def parseupdate(self):
        print "IT IS AN UPDATE!!!!"

    # User Authentication
    def parseauth(self):
        suser = False
        spass = False
        username = ""
        password = ""
        for c in self.data:
            if spass:
                password += c
            if c == '|':
                suser = False
                spass = True
            if suser:
                username += c
            if c == '/':
                suser = True
        self.data = ""
        if username == "" and password == "":
            return "User and Pass are Empty"
        if username == "":
            return "User is Empty"
        if password == "":
            return "Pass is Empty"
        if self.datamgr.authenticate(username, password, self._ip, self._port):
            if self.datamgr.checkonline(username):
                newuser = self.datamgr.getuserobject(username)
                newuser.setip(self._ip)
                self.datamgr.setonline(newuser.getusername())
                return "%s, has Successfully logged In" % username
            else:
                return "User Already Online!"
        else:
            return "Login Error : Username/Password don't match"
    def parseadduser(self):
        count = 0
        sname = False
        suser = False
        spass = False
        name = ""
        username = ""
        password = ""
        for c in self.data:
            if sname:
                name += c
            if c == '|' and count == 1:
                sname = True
                spass = False
            if spass:
                password += c
            if c == '|' and count == 0:
                suser = False
                spass = True
                count += 1
            if suser:
                username += c
            if c == '/':
                suser = True
        newuser = user.User(name, username, password, 0, self._ip)
        self.data = ""
        return self.datamgr.insertUser(newuser)
        # return "A new user %s has been created " % newuser.getname()

    # Set user offline when he quits
    def setoffline(self, username):
        self.datamgr.setoffline(username)

    def getonlinefriends(self, username):
        return self.datamgr.getonlinefriends(username)
