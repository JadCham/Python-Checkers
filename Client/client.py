# from socket import *
import socket
import time
import sys
import atexit
import threading

import chat
import gamep2p


class Client(threading.Thread):
    # Code to run on Exit
    def __init__(self, clientsocket, data):
        self.data = data
        try :
            self.chatlisten = chat.Chat("listen")
            threading.Thread(self.chatlisten.main())
        except:
            print("Error Launching Chat")

        self.gamep2p = gamep2p.Gamep2p('listen')
        threading.Thread(self.gamep2p.main())
        threading.Thread(self.client())
        self.sock = clientsocket

    def setusername(self, username):
        self.username = username

    def setpassword(self, password):
        self.password = password

    def setdata(self, data):
        self.data = data

    def exitprog(self):
        print ("Exiting the program.. Cleaning up")
        # Close the socket
        try:
            # logout user
            flag = False
            self.sock.sendall("isoff:/%s" % self.username)
            self.sock.close()
            print ("Closed Socket")
        except:
            print ("Error while closing socket")
            pass
        sys.exit(1)

    def parseip(self, msg):
        msg = ""
        ip = ""
        sip = False
        for c in msg:
            if sip:
                ip += c
            if c == '/':
                sip = True
        return ip

    def client(self):
        friend = "jad"
        count = 1
        nettuple = ('localhost', 5565)
        atexit.register(self.exitprog)

        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                sock.connect(nettuple)
            except socket.error:
                if count == 5:
                    sys.exit(1)
                count += 1
                print ("Attempt %s : Failed to connect to Server...Trying every 5 Seconds" % count)
                time.sleep(3.0)
                continue

            # Reset Attempts Count
            count = 0
            friend = "jadtest"
            # sock.sendall("adduser:/jadtest1|p@ssw0rd|Jad Chamoun")
            # sock.sendall("msg:/%s|%s" % (self.username, friend))
            # sock.sendall("afriend:/%s|%s" % (username, friend))
            # sock.sendall("greq:/%s|%s" % (self.username, friend))

            Response = "initial"
            # Check Timeout
            olddata = ""
            while True:
                if self.data != olddata:
                    print (self.data)
                    try:
                        d = "%s" % self.data
                        sock.sendall(self.data.encode('ascii'))
                        olddata = self.data
                    except socket.error:
                        print ("Error sending data ")
                try:
                    req = sock.recv(1024).decode('ascii')
                    if req != Response:
                        print (req)
                        if req.__contains__("mip:/"):
                            ip = self.parseip(req)
                            newchat = chat.Chat(ip)
                            threading.Thread(newchat.main())
                        if req.__contains__("gip:/"):
                            ip = self.parseip(req)
                            newgame = gamep2p.Gamep2p(ip)
                            threading.Thread(newgame.main())
                    if req == "" or not req:
                        print ("Connection Disconnected")
                        break
                except socket.timeout:
                    print ("TIME")
                    time.sleep(3.0)
                except:
                    # Wait for 5 seconds and send an online signal
                    print ("ERROR")
                    time.sleep(3.0)
                    sys.exit(1)

username = "jad"
password = "p@ssw0rd"
data = "auth:/%s|%s" % (username, password)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
t = Client(sock, username, password, data)
t.start()
