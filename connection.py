import threading
import socket
import sys

class Client(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.__addr = (host, port)
        self.__socket_client = socket.socket()

    #méthode de connection
    def __connect(self) -> int:
        try :
            self.__socket_client.connect(self.__addr)
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
        self.__socket_client.connect(self.__addr)

    # méthode de dialogue synchrone
    def __dialogue(self):

        mess = ""
        data = ""

        while mess != "kill" and mess != "disconnect" and mess != "reset" and data != "kill" and data != "disconnect" and data != "reset":
            mess = input("client: ")
            self.__socket_client.send(mess.encode())
            data = input("server: ")
            self.__socket_client.recv(1024).decode()
            print(mess)
        self.__socket_client.close()
    
    def send(self):
        self.__socket_client.send()

    def recv(self):
        self.__socket_client.recv()


    def run(self):
        if (self.__connect() ==0):
            self.__dialogue()


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