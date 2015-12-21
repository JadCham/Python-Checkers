import socket
import threading
import select
import time


class Gamep2p:

    def __init__(self, ip):
        self._ip = ip
        self.text = ""

    def settext(self, text):
        self.text = text

    def main(self):

        class Chat_Server(threading.Thread):

                def __init__(self):
                    threading.Thread.__init__(self)
                    self.running = True
                    self.conn = None
                    self.addr = None

                def run(self):
                    host = ''
                    port = 1777
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind((host, port))
                    s.listen(1)
                    self.conn, self.addr = s.accept()
                    while self.running:
                        inputready, outputready, exceptready = select.select([self.conn], [self.conn], [])
                        for input_item in inputready:
                            data = self.conn.recv(1024)
                            if data:
                                print (data)
                            else:
                                break
                        time.sleep(0)

                def kill(self):
                    self.running = False

        class Chat_Client(threading.Thread):

                def __init__(self):
                    threading.Thread.__init__(self)
                    self.host = None
                    self.sock = None
                    self.running = 1

                def run(self):
                    port = 1777
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect((self.host, port))
                    while self.running:
                        inputready, outputready, exceptready = select.select([self.sock], [self.sock], [])
                        for input_item in inputready:
                            data = self.sock.recv(1024)
                            if data:
                                print (data)
                            else:
                                break
                        time.sleep(0)

                def kill(self):
                    self.running = False

        class Text_Input(threading.Thread):
                def __init__(self, main):
                    threading.Thread.__init__(self)
                    self.running = 1
                    self.all = main

                def run(self):
                    old = ""
                    while self.running:
                        if self.all.text != old:
                            print (self.all.text)
                            old = self.all.text

                            try:
                                chat_client.sock.sendall(self.all.text)
                                print ("position sent %s" % self.all.text)
                            except:
                                Exception

                            try:
                                chat_server.conn.sendall(self.all.text)
                                print ("position sent" % self.all.text)
                            except:
                                Exception
                            time.sleep(0)


                def kill(self):
                    self.running = False

        if self._ip == 'listen':
            chat_server = Chat_Server()
            chat_client = Chat_Client()
            chat_server.start()
            text_input = Text_Input(self)
            text_input.start()
            print ("Game P2P Listening")

        else:
            chat_server = Chat_Server()
            chat_client = Chat_Client()
            chat_client.host = self._ip
            text_input = Text_Input(self)
            chat_client.start()
            text_input.start()
            print ("Game P2P Initiated")
