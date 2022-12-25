import socket
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit
import threading


class Client(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__socket_client = socket.socket()
        print("Connexion établie...")

    #méthode de connection
    def __connect(self) -> int:
        try :
            self.__socket_client.connect((self.__host,self.__port))
        except ConnectionRefusedError:
            print ("serveur non lancé ou mauvaise information")
            return -1
        except ConnectionError:
            print ("erreur de connection")
            return -1
        else :
            print ("connexion réalisée")
            return 0

    # méthode de dialogue synchrone
    def __dialogue(self):
        msg = ""
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = input("client: ")
            self.__socket_client.send(msg.encode())
            msg = self.__socket_client.recv(1024).decode()
            print(msg)
        self.__socket_client.close()


    def run(self):
        if (self.__connect() ==0):
            self.__dialogue()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)


        self.lab = QLabel("Saisissez votre commande")
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
        self.aide = QPushButton("?")
        self.ipserv = QLabel("IP serveur")
        self.ip = QLineEdit("")
        self.port = QLineEdit("")
        self.connection = QPushButton("Connection")

        grid.addWidget(self.lab, 0, 0, 1, 2)
        grid.addWidget(self.text, 1, 0, 1, 2)
        grid.addWidget(self.choix, 1, 2, 1, 2)
        grid.addWidget(self.info, 3, 0, 1, 4)
        grid.addWidget(self.ok, 2, 0, 1, 2)
        grid.addWidget(self.okcbox, 2, 2, 1, 2)
        grid.addWidget(self.quit, 4, 0, 1, 4)
        grid.addWidget(self.reset, 5, 0, 1, 4)
        grid.addWidget(self.kill, 6, 0, 1, 4)
        grid.addWidget(self.aide,0, 3)
        grid.addWidget(self.ipserv,7, 0)
        grid.addWidget(self.ip,7, 1)
        grid.addWidget(self.port,7, 2)
        grid.addWidget(self.connection, 7, 3)


        self.okcbox.clicked.connect(self.__actionOkCbox)
        self.ok.clicked.connect(self.__actionOkText)
        self.quit.clicked.connect(self.__actionQuitter)
        self.kill.clicked.connect(self.__actionKill)
        self.reset.clicked.connect(self.__actionReset)
        self.aide.clicked.connect(self.__actionAide)
        self.connection.clicked.connect(self.__actionConnect)
        self.setWindowTitle("Mon Application")

    
    def __actionConnect(self):
        addr=self.line_edit3.text()
        port = int(addr.split(":")[1])
        ip = addr.split(":")[0]
        socket_client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_client.connect(ip, port)
        print("Connexion établie ...")
        QMessageBox.information(self, "Conexion", "Connexion réussie")


    def __actionOkText(self):
        mess=self.text.text()
        socket_client.send(mess.encode())
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
        mess= "kill"
        socket_client.send(mess.encode())

    def __actionReset(self):
        mess= "reset"
        socket_client.send(mess.encode())


    def __actionAide(self):
        QMessageBox.information(self, "Aide","Choisissez une information du pc, de la vm que vous voulez récupérer (l'os, le nom, l'ip, ...).")


    def CSV(self):

        try:
            with open("serv.csv") as file:
                col_headers = ['IP', 'PORT']
                self.table.setHorizontalHeaderLabels(col_headers)
                reader = csv.reader(file, delimiter=":")
                for i, row in enumerate(reader):
                    for j, col in enumerate(row):
                        self.table.setItem(i, j, QTableWidgetItem(col))
        except:
            with open("serv.csv", 'w') as file:
                file.write('')


        self.table.show()
        self.show()


if __name__ == '__main__':

    if len(sys.argv) < 3:
        client = Client("127.0.0.1",15001)
    else :
        host = sys.argv[1]
        port = int(sys.argv[2])
        # création de l'objet client qui est aussi un thread
        client = Client(host,port)
    #démarrage de la thread client
    client.start()
    client.join()


    #print(f"localhost {port}")
    #socket_client.connect(("localhost"))
    print("Connexion établie...")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()