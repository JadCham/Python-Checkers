<<<<<<< Updated upstream:Server/server.py
import socket
import sys
import threading
import atexit

import datamanager
import requestmanager


class ClientServer(threading.Thread):

    SendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.client_sock = socket
        self.datamgr = datamanager.DataManager("localhost", "liwaa", "p@ss0rd", "testDatabase")
        self.datamgr.setalloff()
        self.flag = True

    # Code to run on Exit
    def exitprog(self):
        self.flag = False
        print "Exiting Server.. Cleaning up"
        self.client_sock.close()
        sys.exit(1)

    def run(self):
        flag = True
        self.client_sock.settimeout(10.0)
        username = ""
        while flag:
            try:
                message = self.client_sock.recv(1024)
                if message == "" or not message:
                    print "Etil hayda"
                    flag = False
                    break
                print message
                self.reqmgr = requestmanager.RequestManager(message, client_addr[0], client_addr[1], self)
                message = ""
                response = self.reqmgr.parsedata()
                if response.__contains__("has Successfully logged In"):
                    for c in response:
                        if c == ',':
                            break
                        username += c
                    print "User %s is in " % username
                # print response
                self.client_sock.sendall(response)
            except KeyboardInterrupt:
                self.reqmgr.setoffline(username)
                atexit.register(self.exitprog)
                self.client_sock.close()
                sys.exit(1)
            except socket.timeout:
                if username != "":
                    self.client_sock.sendall(self.reqmgr.getonlinefriends(username))
                continue
            except socket.error, e:
                print "Error %s %s" % (username, e.message)
                if username != "":
                    self.reqmgr.setoffline(username)
                break
        self.reqmgr.setoffline(username)
        self.client_sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('localhost', 5565)
sock.bind(address)


sock.listen(20)
print "*************KebbeBlaban*************"
print "Server is Up and Running and Waiting "
print "*************************************"
while True:
    client_sock, client_addr = sock.accept()
    t = ClientServer(client_sock)
    t.start()
=======
import socket
import sys
import threading
import datamanager
import user
import requestmanager
import  data
import atexit


class ClientServer(threading.Thread):

    SendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.client_sock = socket
        self.datamgr = datamanager.DataManager("localhost", "liwaa", "p@ss0rd", "testDatabase")
        self.flag = True

    # Code to run on Exit
    def exitprog(self):
        self.flag = False
        print "Exiting Server.. Cleaning up"
        client_sock.close()
        sys.exit(1)

    def run(self):
        flag = True
        client_sock.settimeout(10.0)
        username = ""
        while flag:
            try:
                message = client_sock.recv(1024)
                if message == "" or not message:
                    print "Etil hayda"
                    flag = False
                    break
                print message
                self.reqmgr = requestmanager.RequestManager(message, client_addr[0], client_addr[1], self)
                message = ""
                response = self.reqmgr.parsedata()
                if response.__contains__("has Successfully logged In"):
                    for c in response:
                        if c == ',':
                            break
                        username += c
                    print "User %s is in " % username
                # print response
                client_sock.sendall(response)
            except KeyboardInterrupt:
                self.reqmgr.setoffline(username)
                atexit.register(self.exitprog)
                client_sock.close()
                sys.exit(1)
            except socket.timeout:
                client_sock.sendall(self.reqmgr.getonlinefriends(username))
                continue
            except socket.error, e:
                print "Error %s %s" % (username, e.message)
                self.reqmgr.setoffline(username)
                break
        self.reqmgr.setoffline(username)
        client_sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('localhost', 55655)
sock.bind(address)


sock.listen(20)
print "*************KebbeBlaban*************"
print "Server is Up and Running and Waiting "
print "*************************************"
while True:
    client_sock, client_addr = sock.accept()
    t = ClientServer(client_sock)
    t.start()
>>>>>>> Stashed changes:server.py
