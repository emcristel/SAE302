import socket
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit, QTextBrowser
from PyQt6.QtCore import QThread
import threading



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
        self.info = QTextBrowser()
        self.info.setReadOnly(True)
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
        self.quit.clicked.connect(self.__actionDisconnect)
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
                self.__socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__socket_client.connect((host, port))
                self.thread_reception = ThreadReception(self.__socket_client, self.info)
                self.thread_reception.start()
                self.statut.setText("Connecté")
                self.statut.setStyleSheet("background-color: blue; font-weight: bold; color: black;")
                QMessageBox.information(self, "Connexion", "Connexion réussie")
            except:
                QMessageBox.warning(self, "Connexion", "Connexion échouée")
            

    def __actionDisconnect(self):
            if self.statut.text() == 'Connecté':
                self.__socket_client.send("close".encode())
                self.__socket_client.close()
                self.thread_reception.terminate()
                self.info.clear()
                self.statut.setText("Déconnecté")
                self.statut.setStyleSheet("background-color: red; font-weight: bold; color: black;")
                QMessageBox.information(self, "Deconnexion", "Deconnexion réussie")
            else:
                QMessageBox.warning(self, "Deconnexion", "Déja déconnecté")


    def __actionOkText(self):
        mess = self.text.text()
        self.__socket_client.send(mess.encode())
        self.text.clear()

    def __actionOkCbox(self):
        mess = self.choix.currentText()
        self.__socket_client.send(mess.encode())

    
    def __actionKill(self):
        if self.statut.text() == 'Connecté':
            self.__socket_client.send("close".encode())
            self.__socket_client.close()
            self.thread_reception.terminate()
            self.info.clear()
            self.statut.setText("Déconnecté")
            self.statut.setStyleSheet("background-color: red; font-weight: bold; color: black;")
            QMessageBox.information(self, "Deconnexion", "Deconnexion réussie")
        else:
            QMessageBox.warning(self, "Deconnexion", "Déja déconnecté")
        

    def __actionReset(self):
        if self.statut.text() == 'Connecté':
            self.__socket_client.send("close".encode())
            self.__socket_client.close()
            self.thread_reception.terminate()
            self.info.clear()
            self.statut.setText("Déconnecté")
            self.statut.setStyleSheet("background-color: red; font-weight: bold; color: black;")
            QMessageBox.information(self, "Deconnexion", "Deconnexion réussie")
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.statut.setText("Connecté")
            self.statut.setStyleSheet("background-color: blue; font-weight: bold; color: black;")
            QMessageBox.information(self, "Connecté", "Connexion réussie")
        else:
            QMessageBox.warning(self, "Deconnexion", "Déja déconnecté")


    def __actionAide(self):
        QMessageBox.information(self, "Aide","Choisissez une information du pc, de la vm que vous voulez récupérer (l'os, le nom, l'ip, ...).")



####                            ####
#### PARTIE THREAD DE RECEPTION ####
####                            ####

class ThreadReception(QThread):
    def __init__(self, __socket_client, info):
        super().__init__()
        self.socket_client = __socket_client
        self.info = info
        self.exit_event = threading.Event()

    def run(self):
        flag = True
        while flag == True:
            if self.exit_event.is_set():
                print ("exit")
                flag = False
            try:
                data = self.socket_client.recv(1024)
                self.info.append(f"Client> {data.decode('utf-8')}")
                # Refresh the QPlainTextEdit
                self.info.verticalScrollBar().setValue(self.serverreply.verticalScrollBar().maximum())
                self.info.update()
                # Create a log file for each client
                # Write the data received from the client to the log file
            except:
                pass

    def stop(self):
        self.exit_event.set()
        self.wait()


### MAIN ###

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()