import socket
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.lab = QLabel("Saisir votre message")
        self.text = QLineEdit("")
        self.info = QTextEdit("")
        self.choix = QComboBox()
        self.choix.addItem("OS")
        self.choix.addItem("RAM")
        self.choix.addItem("CPU")
        self.choix.addItem("IP")
        self.choix.addItem("Name")
        self.ok = QPushButton("Ok")
        self.okcbox = QPushButton("Ok")
        self.quit = QPushButton("Quitter")
        self.kill = QPushButton("Kill")
        self.reset = QPushButton("Reset")
        self.aide =QPushButton("?")


        grid.addWidget(self.lab, 0, 0, 1, 2)
        grid.addWidget(self.text, 1, 0, 1, 2)
        grid.addWidget(self.choix, 1, 2, 1, 2)
        grid.addWidget(self.info, 3, 0, 1, 4)
        grid.addWidget(self.ok, 2, 0, 1, 2)
        grid.addWidget(self.okcbox, 2, 2, 1, 2)
        grid.addWidget(self.quit, 4, 0, 1, 4)
        grid.addWidget(self.reset, 5, 0, 1, 4)
        grid.addWidget(self.kill, 6, 0, 1, 4)
        grid.addWidget(self.aide,7, 3)


        self.okcbox.clicked.connect(self.__actionOkCbox)
        self.ok.clicked.connect(self.__actionOkText)
        self.quit.clicked.connect(self.__actionQuitter)
        self.kill.clicked.connect(self.__actionKill)
        self.reset.clicked.connect(self.__actionReset)
        self.aide.clicked.connect(self.__actionAide)
        self.setWindowTitle("Mon Application")


    def __actionOkText(self):
        mess=self.text.text()
        socket_client.send(mess.encode())
        print("Message envoyé")
        data = socket_client.recv(1024).decode()
        self.info.append(f"{data}")


    def __actionOkCbox(self):
        
        socket_client.send(self.choix.currentText().encode())
        data = socket_client.recv(1024).decode()
        self.info.append(f"{data}")

        
        """""
        try:

            if self.choix.currentText() == "OS":
                msg="os"
                socket_client.send(msg.encode())
                data = socket_client.recv(1024).decode()
                self.info.append(f"{data}")

            elif self.choix.currentText() == "CPU":
                msg="CPU"
                socket_client.send(msg.encode())
                data = socket_client.recv(1024).decode()
                self.info.append(f"{data}")

            elif self.choix.currentText() == "IP":
                msg="IP"
                socket_client.send(msg.encode())
                data = socket_client.recv(1024).decode()
                self.info.append(f"{data}")

            elif self.choix.currentText() == "RAM":
                msg="RAM"
                socket_client.send(msg.encode())
                data = socket_client.recv(1024).decode()
                self.info.append(f"{data}")

            else:
                msg="Name"
                socket_client.send(msg.encode())
                data = socket_client.recv(1024).decode()
                self.info.append(f"{data}")

        except ValueError:
            QMessageBox.critical(self, "Erreur")
        """


    def __actionQuitter(self):
        mess= "disconnect"
        socket_client.send(mess.encode())


    
    def __actionKill(self):
        socket_client.close()
        QCoreApplication.exit(0)

    def __actionReset(self):
        QCoreApplication.exit(0)

    def __actionAide(self):
        QMessageBox.information(self, "Aide","Choisissez une information du pc, de la vm que vous voulez récupérer (l'os, le nom, l'ip, ...).")




if __name__ == '__main__':
    menu = input("Pour se connecter au serveur n°1 taper 1. Pour se connecter au serveur n°2 taper 2 : ")
    if menu == "1":
        port = 10000
    else:
        port = 10001

    socket_client = socket.socket()
    print(f"localhost {port}")
    socket_client.connect(("localhost", port))
    print("Connexion établie...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()