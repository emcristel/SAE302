import socket
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit
import threading
import csv


####                         ####
#### PARTIE THREADING CLIENT ####
####                         ####


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

    def connection(self):
        self.__socket_client.connect((self.__host, self.__port))

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


####                    ####
#### PARTIE FICHIER CSV ####
####                    ####


class CSV(QWidget):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        grid = QGridLayout()
        widget.setLayout(grid)
        self.CSV()

    def CSV(self):
        self.setGeometry(1000, 1000, 1000, 1000)
        self.setWindowTitle("QTableWidget Example")

        self.table = QTableWidget(self)
        self.table.setRowCount(10)
        self.table.setColumnCount(2)

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


####                            ####
#### PARTIE INTERFACE GRAPHIQUE ####
####                            ####


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.etat = QLabel("Déconnecté")
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
        self.ip = QLineEdit("127.0.0.1")
        self.port = QLineEdit("10000")
        self.connection = QPushButton("Connection")

        grid.addWidget(self.etat, 0, 0)
        self.etat.setStyleSheet("background-color: red; font-weight: bold; color: black;")
        grid.addWidget(self.lab, 1, 0, 1, 2)
        grid.addWidget(self.text, 2, 0, 1, 2)
        grid.addWidget(self.choix, 2, 2, 1, 2)
        grid.addWidget(self.info, 4, 0, 1, 4)
        grid.addWidget(self.ok, 3, 0, 1, 2)
        grid.addWidget(self.okcbox, 3, 2, 1, 2)
        grid.addWidget(self.quit, 5, 0, 1, 4)
        grid.addWidget(self.reset, 6, 0, 1, 4)
        grid.addWidget(self.kill, 7, 0, 1, 4)
        grid.addWidget(self.aide, 1, 3)
        grid.addWidget(self.ipserv, 8, 0)
        grid.addWidget(self.ip, 8, 1)
        grid.addWidget(self.port, 8, 2)
        grid.addWidget(self.connection, 8, 3)


        self.okcbox.clicked.connect(self.__actionOkCbox)
        self.ok.clicked.connect(self.__actionOkText)
        self.quit.clicked.connect(self.__actionQuitter)
        self.kill.clicked.connect(self.__actionKill)
        self.reset.clicked.connect(self.__actionReset)
        self.aide.clicked.connect(self.__actionAide)
        self.connection.clicked.connect(self.__actionConnect)
        self.setWindowTitle("Mon Application")

    
    ## ACTION BOUTONS ##

    def __actionConnect(self):

        host = str(self.ip.text())
        port = int(self.port.text())

        if self.etat.text() == 'Déconnecté':
            try:
                self.__socket_client = Client(host, port)
                self.__socket_client.connection()
                self.etat.setText("Connecté")
                self.etat.setStyleSheet("backgroung-color: blue; font-weight: bold; color: black;")

            except ConnectionRefusedError:
                mess = QMessageBox.warning(self, "Conexion", "Erreur du serveur")

                return -1
            except ConnectionError:
                print("Erreur de connection")
                return -1
            except ConnectionResetError:
                print('Erreur de connection après reset')
                return -1
            else:
                mess = "Connexion réussie !"
                return 0
        else:
            mess = QMessageBox.warning(self, "Conexion", "Connection déjà en cours")
            mess.exec()



    def __actionOkText(self):
        mess=self.text.text()
        self.__socket_client.send(mess.encode())
        data = self.__socket_client.recv(1024).decode()
        self.info.append(f"{data}")


    def __actionOkCbox(self):
        
        self.__socket_client.send(self.choix.currentText().encode())
        data = self.__socket_client.recv(1024).decode()
        self.info.append(f"{data}")

               


    def __actionQuitter(self):
        mess= "disconnect"
        self.__socket_client.send(mess.encode())

    
    def __actionKill(self):
        mess= "kill"
        self.__socket_client.send(mess.encode())

    def __actionReset(self):
        mess= "reset"
        self.__socket_client.send(mess.encode())


    def __actionAide(self):
        QMessageBox.information(self, "Aide","Choisissez une information du pc, de la vm que vous voulez récupérer (l'os, le nom, l'ip, ...).")


### MAIN ###

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