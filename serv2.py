import socket
import platform
import threading
import psutil


serveur_socket=socket.socket()
serveur_socket.bind(("0.0.0.0", 10000))
serveur_socket.listen(5)


# Event for stopping threads
thread_event = threading.Event()

def clients():
    global client

    while True and not thread_event.is_set():
        try: 
            print("Serveur démarré en attente de connexion...")
            client, addr = serveur_socket.accept()
            print("Connection réussie ...")
            client.send(f"Connection éatblie avec le serveur {platform.node()}, son IP est : {socket.gethostbyname(socket.gethostname())}".encode())
            threading.Thread(target=thread_reception, args=[client]).start()
        except Exception as e:
            print(f'Error: {e}')
            pass


def thread_reception(client):
    import os
    while True and not thread_event.is_set():
        data = client.recv(1024).decode()
        print(data)

        if data == "os" or data == "OS" :
            os = platform.system()
            msg=str(f"OS: {os}")
            client.send(msg.encode())

        elif data == "Name" or data == "NAME" or data == "name" :
            nom = platform.node()
            msg=str(f"Nom: {nom}")
            client.send(msg.encode())

        elif data == "ip" or data == "IP" :
            ip = socket.gethostbyname(socket.gethostname())
            msg=str(f"IP: {ip}")
            client.send(msg.encode())

        elif data == "cpu" or data == "CPU" :
            cpu = psutil.cpu_percent()
            msg=str(f"CPU USAGE: {cpu}%")
            client.send(msg.encode())

        elif data == "ram" or data == "RAM" :
            ram = round(psutil.virtual_memory().total / (1024.0 **3))
            msg=str(f"RAM: {ram}GB")
            client.send(msg.encode())

        elif data == "close" or data == "CLOSE" or data == "Close":
            client.close()
            clients()
            print("Connection fermée")


        elif data == "kill" or data == "KILL" or data == "Kill":
            client.close()
            clients()
            print("Connection fermée")
            socket.close()
            print("Serveur fermé")
            break

        elif data == "kill" or data == "KILL" or data == "Kill":
            client.close()
            clients()
            print("Connection fermée")
            break

        else:
            cmd = data
            verif = os.system(cmd)
            msg = os.popen(cmd).read()

            if verif == 0:

                if msg != "":
                    client.send(msg.encode())    
                else:
                    client.send(f"{cmd} ok".encode())
            else:
                msg=str(f'{cmd} ne peut pas être lancée')
                client.send(msg.encode())
            


def main():
    threading.Thread(target=clients).start()

if __name__ == "__main__":
    main()


            