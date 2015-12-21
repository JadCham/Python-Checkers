import sqlite3
import sys
import user


class DataManager:

    # Constructor
    def __init__(self, host, user, password, database):
        self.sethost(host)
        self._user = user
        self._password = password
        self._database = database
        self.connect()

    # Connect Database
    def connect(self):
        try:
            self.db_connection = sqlite3.connect('mydb.db')
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)
        self.cursor = self.db_connection.cursor()

    # Setters
    def sethost(self, host):
        self._host = host

    def setuser(self, user):
        self._user = user

    def setpassword(self, password):
        self._password = password

    def setdatabase(self, database):
        self._database = database

    # Getters
    def gethost(self):
        return self._host

    def getuser(self):
        return self._user

    def getpassword(self):
        return self._password

    def getdatabase(self):
        return self._database

    # Print Data
    def printall(self, data):
        print "There are %d data items" % len(data)
        for i,d in enumerate(data):
            print "%d --- "% i, d

    # Get User Object
    def getuserobject(self, username):
        query_name = "SELECT NAME FROM USER WHERE USERNAME=\"%s\"" % username
        query_password = "SELECT PASSWORD FROM USER WHERE USERNAME=\"%s\"" % username
        query_score = "SELECT SCORE FROM USER WHERE USERNAME=\"%s\"" % username
        query_ip = "SELECT IP FROM USER WHERE USERNAME=\"%s\"" % username
        try:
            self.cursor.execute(query_name)
            name = self.cursor.fetchone()[0]
            self.cursor.execute(query_password)
            password = self.cursor.fetchone()[0]
            self.cursor.execute(query_score)
            score = self.cursor.fetchone()[0]
            self.cursor.execute(query_ip)
            ip = self.cursor.fetchone()[0]
            newuser = user.User(name, username, password, score, ip)
            return newuser
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)

    # Get User Name from ID
    def getnamefromid(self, currid):
        query_name = "SELECT NAME FROM USER WHERE ID=\"%s\"" % currid
        try:
            self.cursor.execute(query_name)
            name = self.cursor.fetchone()[0]
            return name
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)

    # Get ID from Username
    def getidfromuser(self, username):
        query_name = "SELECT ID FROM USER WHERE USERNAME=\"%s\"" % username
        try:
            self.cursor.execute(query_name)
            name = self.cursor.fetchone()[0]
            return name
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)

    # check if user is on
    def isonline(self, currid):
        query = "SELECT ONLINE FROM USER WHERE ID=\"%s\"" % currid
        try:
            self.cursor.execute(query)
            online = self.cursor.fetchone()[0]
            if online == 1:
                return True
            else:
                return False
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)

    # Add Friend
    def addfriend(self, username, friend):
        #addfriend to user
        query = "SELECT FRIENDS FROM USER WHERE USERNAME=\"%s\"" % username
        try:
            self.cursor.execute(query)
            friends = self.cursor.fetchone()[0]
            fid = self.getidfromuser(friend)
            friendid = "%s|" % fid
            if friends.__contains__(friendid):
                return "Already Friends"
            else:
                friends += friendid
                query = "UPDATE USER SET FRIENDS = \"%s\" WHERE USERNAME= \"%s\"" % (friends, username)
                try:
                    self.cursor.execute(query)
                    self.db_connection.commit()
                except sqlite3.Error, e:
                    print e.args[0]
                    sys.exit(1)
                # return "Added Friends"
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)
        #Put request on friend's list
        query = "SELECT FRIENDS FROM USER WHERE USERNAME=\"%s\"" % friend
        try:
            self.cursor.execute(query)
            friends = self.cursor.fetchone()[0]
            fid = self.getidfromuser(username)
            friendid = "%s!|" % fid
            if friends.__contains__(friendid):
                return "Already Friends"
            else:
                friends += friendid
                query = "UPDATE USER SET FRIENDS = \"%s\" WHERE USERNAME= \"%s\"" % (friends, friend)
                try:
                    self.cursor.execute(query)
                    self.db_connection.commit()
                except sqlite3.Error, e:
                    print e.args[0]
                    sys.exit(1)
                return "Added Friends"
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)

    #accept friend
    def acceptfriend(self, username, friend):
        query = "SELECT FRIENDS FROM USER WHERE USERNAME=\"%s\"" % username
        try:
            self.cursor.execute(query)
            friends = self.cursor.fetchone()[0]
            fid = self.getidfromuser(friend)
            friendid = "%s|" % fid
            newfriends = ""
            for c in friends:
                if c != "!":
                    newfriends += c
            query = "UPDATE USER SET FRIENDS = \"%s\" WHERE USERNAME= \"%s\"" % (newfriends, username)
            try:
                self.cursor.execute(query)
                self.db_connection.commit()
            except sqlite3.Error, e:
                print e.args[0]
                sys.exit(1)
                # return "Added Friends"
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)

    #reject friend request
    def rejectfriend(self, username, friend):
        query = "SELECT FRIENDS FROM USER WHERE USERNAME=\"%s\"" % username
        try:
            self.cursor.execute(query)
            friends = self.cursor.fetchone()[0]
            fid = self.getidfromuser(friend)
            friendid = "%s|" % fid
            newfriends = ""
            for c in friends:
                if c != "!" and c != fid:
                    newfriends += c
            query = "UPDATE USER SET FRIENDS = \"%s\" WHERE USERNAME= \"%s\"" % (newfriends, username)
            try:
                self.cursor.execute(query)
                self.db_connection.commit()
            except sqlite3.Error, e:
                print e.args[0]
                sys.exit(1)
                # return "Added Friends"
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)

    # check if user is on
    def setonline(self, username):
        query = "UPDATE USER SET ONLINE = 1 WHERE USERNAME= \"%s\"" % username
        try:
            self.cursor.execute(query)
            self.db_connection.commit()
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)

    # check if user is on
    def setoffline(self, username):
        query = "UPDATE USER SET ONLINE = 0 WHERE USERNAME= \"%s\"" % username
        try:
            self.cursor.execute(query)
            self.db_connection.commit()
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)
    # Check Online Friends
    def getonlinefriends(self, username):
        query = "SELECT FRIENDS FROM USER WHERE USERNAME=\"%s\"" % username
        self.cursor.execute(query)
        friends = self.cursor.fetchone()[0]
        currid = 0
        names = ""
        temp = ""
        if friends == None:
            return "#"
        for c in friends:
            if c == '|':
                currid = temp
                temp = ""
                if self.isonline(currid):
                    name = self.getnamefromid(currid)
                    name += "|"
                    names += name
            else:
                temp += c
        if names == "":
            names = "!"
        names += "/"
        currid = 0
        temp = ""
        for c in friends:
            if c == '|':
                currid = temp
                temp = ""
                if self.isonline(currid):
                    continue
                else:
                    name = self.getnamefromid(currid)
                    name += "|"
                    names += name
            else:
                temp += c
        return names

    #Set all users offline
    def setalloff(self):
        query = "UPDATE USER SET ONLINE = 0"
        try:
            self.cursor.execute(query)
            self.db_connection.commit()
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)
    # Insert User
    def insertUser(self, user):
        userquery = "SELECT USERNAME FROM USER WHERE USERNAME = \"%s\" " % user.getusername
        try:
            self.cursor.execute(userquery)
            self.db_connection.commit()
            result = self.cursor.fetchone()[0]
            return "Username already taken!"
        except:
            try:
                query = "INSERT INTO USER " + \
                        "(NAME,USERNAME,PASSWORD,SCORE) VALUES (\'%s\', \'%s\', \'%s\', \'%d\');" \
                        % (user.getname(), user.getusername(), user.getpassword(), user.getscore())
                print query
                self.cursor.execute(query)
                self.db_connection.commit()
                return "User %s has been created" % user.getname()
            except sqlite3.Error, e:
                print e.args[0]
                if e.args.count("UNIQUE constraint failed: USER.USERNAME"):
                    return "Username already taken!"
                sys.exit(1)

    def checkonline(self, username):
        try:
            query = "SELECT ONLINE FROM USER WHERE " +\
                                "USERNAME = \"%s\";"\
                    % username
            print query
            self.cursor.execute(query)
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)
        result = self.cursor.fetchone()[0]
        print "CHECKONLINE :: %s" % result
        if result == 1:
            return False
        return True
    # Authenticate user
    def authenticate(self, username, password, ip, port):
        try:
            query = "SELECT * FROM USER WHERE " +\
                                "USERNAME = \"%s\" AND PASSWORD = \"%s\";"\
                    % (username, password)
            print query
            self.cursor.execute(query)
        except sqlite3.Error, e:
            print e.args[0]
            sys.exit(1)
        try:
            result = self.cursor.fetchone()[0]
        except:
            return False
        if len(result) > 0:
            query_ip = "UPDATE USER SET IP = \"%s\" WHERE USERNAME= \"%s\"" % (ip, username)
            query_port = "UPDATE USER SET PORT = \"%s\" WHERE USERNAME= \"%s\"" % (port, username)
            try:
                self.cursor.execute(query_port)
                self.db_connection.commit()
                self.cursor.execute(query_ip)
                self.db_connection.commit()
                return True
            except sqlite3.Error, e:
                print e.args[0]
                sys.exit(1)
        else:
            return False
