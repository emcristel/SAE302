import socket
import platform
import psutil
import netaddr # install with pip install netaddr
import netifaces # install with pip install netifaces
import os

msg = ""
data = ""


while msg!= "kill" and data!= "kill":
    serveur_socket=socket.socket()
    serveur_socket.bind(("127.0.0.1", 10001))
    serveur_socket.listen(1)
    print("Serveur démarré...")

    while msg!="kill" and msg!="reset" and data!="kill" and data!="reset":
        serv, addr = serveur_socket.accept()

        while msg!= "kill" and msg!="reset" and msg!="disconnect" and data!= "kill" and data!="reset" and data!="disconnect":
            data = serv.recv(1024).decode()
            print(data)

            if data == "os" or data == "OS" :
                os= platform.system()
                msg=str(f"Operating system: {os}")
                serv.send(msg.encode())

            elif data == "cpu" or data == "CPU" :
                cpu =  psutil.cpu_percent(4)
                msg=str(f"CPU: {cpu}")
                serv.send(msg.encode())
            
            elif data == "ip" or data == "IP" :
                netifaces.interfaces()
                adresse_ip = netifaces.ifaddresses('en0')[2][0]['addr']
                netaddr_adresse_ip = netaddr.IPAddress(adresse_ip)
                msg=str(f"IP: {netaddr_adresse_ip}")
                serv.send(msg.encode())

            elif data == "ram" or data == "RAM" :
                ram=psutil.virtual_memory()[2]
                msg=str(f'RAM memory % used:{ram}')
                serv.send(msg.encode())

            elif data == "name" or data == "Name" :
                name=platform.node()
                msg=str(f"Mon nom est: {name}")
                serv.send(msg.encode())
            
            elif data.startswith("DOS:mkdir"):
                nom = data.split()[1]
                os.mkdir(nom)
                msg = msg=str(f"Le dossier {nom} a été créé.")
                serv.send(msg.encode())

            elif data.startswith("ping"):
                address = data.split()[1]
                os.system("ping -c 1 " + address)
                msg = msg=str(f"ping: {address}")
                serv.send(msg.encode())

            else:
                msg=input("serveur -->")
                serv.send(msg.encode())


        serv.close()

        rep=input("continuer la discussion (y/n):")
        if rep =='n':
            break

if data == "kill" or msg == "kill":
    serveur_socket.close()