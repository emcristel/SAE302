import socket

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
#            msg=input("serveur -->")
            serv.send(data.encode())

        serv.close()

        rep=input("continuer (y/n):")
        if rep =='n':
            break

serveur_socket.close()