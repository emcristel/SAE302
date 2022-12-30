import socket
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit
import threading


####                         ####
#### PARTIE THREADING CLIENT ####
####                         ####


class Client(threading.Thread):


    def __init__(self, host, port):
        super().__init__()
        self.__host = host
        self.__port = port
        self.__socket_client = socket.socket()
        self.__thread = None
        
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
        mess = ""
        self.__thread = threading.Thread(target=self.__recv, args=[self.__socket_client, ])
        self.__thread.start()
        while mess != "kill" and mess != "disconnect" and mess != "reset":
            mess = self.__send()
        self.__thread.join()
        self.__socket_client.close()
    

    def send(self, mess):
        try:
            self.__socket_client.send(mess.encode())
            data = self.__socket_client.recv(1024).decode()
        except:
            print("Erreur d'envoi")
        else:
            return data


    def __send(self):
        mess = input("client:")
        try:
            self.__socket.send(mess.encode())
        except BrokenPipeError:
            print("Erreur")


    def recv(self, socket_client):
        mess=""
        while mess != "kill" and mess != "disconnect" and mess != "reset":
            mess = socket_client.recv(1024).decode()
            input("Serveur:" )
            print(mess)


    def run(self):
        if (self.__connect() ==0):
            self.__dialogue()


### MAIN ###


if __name__=="__main__":
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
    print("Connexion établie...")



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

        self.statut = QLabel("Déconnecté")
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

        grid.addWidget(self.statut, 0, 0)
        self.statut.setStyleSheet("background-color: red; font-weight: bold; color: black;")
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

        if self.statut.text() == 'Déconnecté':
            try:
                self.__socket_client = Client(host, port)
                self.__socket_client.connection()
                self.statut.setText("Connecté")
                self.statut.setStyleSheet("background-color: blue; font-weight: bold; color: black;")

            except ConnectionRefusedError:
                QMessageBox.warning(self, "Conexion", "Erreur du serveur")
                return -1
            else:
                QMessageBox.information(self, "Connexion", "Connexion réussie")
                return 0
        else:
            QMessageBox.warning(self, "Conexion", "Connection déjà en cours")
            

    def __actionOkText(self):

        self.__socket_client = Client(mess)
        mess = self.text.text()
        self.__socket_client.send(mess.encode())
        data = self.__socket_client.recv(1024).decode()
        self.info.append(f"{data}")


    def __actionOkCbox(self):
        mess = self.choix.currentText()
        self.__socket_client.send(mess.encode())
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
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()