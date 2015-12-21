# from PyQt5 import QtCore, QtGui, QtWidgets
# from checkersGame_ui import Ui_MainWindow
# import User
# import resources, ChatManager
# import GameManager
import client
import socket


class CheckerGame:

    def main(self):
        # import sys
        # app = QtWidgets.QApplication(sys.argv)
        # MainWindow = QtWidgets.QMainWindow()
        #
        # #Create The Players
        # Self = User.User("Liwaa Awar", "liwaa9", "", "127.0.0.1", "D")
        # Opponent = User.User("Jad Chamoun", "jadch", "", "1.1.1.1", "L")
        #
        # #Create Managers
        # ChatMngr = ChatManager.ChatManager(Self, Opponent)
        # GameMngr = GameManager.GameManager(Self, Opponent)
        #
        # #Initialize UI
        # ui = Ui_MainWindow()
        # ui.setupUi(MainWindow, ChatMngr, GameMngr, Self, Opponent)
        # MainWindow.showMaximized()
        # sys.exit(app.exec_())

        # Start the Client to Connect to server and listen to P2P
        self.username = "jad"
        self.password = "p@ssw0rd"
        self.data = "auth:/%s|%s" % (self.username, self.password)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.t = client.Client(self.sock, self.username, self.password, self.data)
        self.t.start()