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
    serveur_socket.bind(("127.0.0.1", 10000))
    serveur_socket.listen(1)
    print("Serveur démarré...")

    while msg!="kill" and msg!="reset":
        connect, addr = serveur_socket.accept()

        while msg!= "kill" and msg!="reset" and msg!="disconnect":
            data = connect.recv(1024).decode()
            print ("Reçu du client: ", data)

            if data == "os" or data == "OS" :
                os= platform.system()
                msg=str(f"Operating system: {os}")
                connect.send(msg.encode())

            elif data == "cpu" or data == "CPU" :
                cpu =  psutil.cpu_percent(4)
                msg=str(f"CPU: {cpu}")
                connect.send(msg.encode())
            
            elif data == "ip" or data == "IP" :
                netifaces.interfaces()
                adresse_ip = netifaces.ifaddresses('en0')[2][0]['addr']
                netaddr_adresse_ip = netaddr.IPAddress(adresse_ip)
                msg=str(f"IP: {netaddr_adresse_ip}")
                connect.send(msg.encode())

            elif data == "ram" or data == "RAM" :
                ram=psutil.virtual_memory()[2]
                msg=str(f'RAM memory % used:{ram}')
                connect.send(msg.encode())

            elif data == "name" or data == "Name" :
                name=platform.node()
                msg=str(f"Mon nom est: {name}")
                connect.send(msg.encode())

            elif data == "disconnect":
                rien = ""
                connect.send(rien.encode())
            
            elif data == "kill":
                rien = ""
                connect.send(rien.encode())

            elif data == "kill":
                rien = ""
                connect.send(rien.encode())


            else: 
                cmd = data
                verif = os.system(cmd)
                msg = os.popen(cmd).read()

                if verif == 0:

                    if msg != "":
                        connect.send(msg.encode())    
                    else:
                        connect.send(f"{cmd} ok".encode())
                else:
                    msg=str(f'{cmd} ne peut pas être lancée')
                    connect.send(msg.encode())
            

        
        connect.close()
        print ("Connection fermé")
    serveur_socket.close()
    print("Serveur fermé")


if data == "kill" or msg == "kill":
    serveur_socket.close()
    print ("SERVEUR FERMÉ !")