import socket

serveur_socket=socket.socket()
serveur_socket.bind(("127.0.0.1", 10000))
serveur_socket.listen(1)
print("Serveur démarré...")

while True:
    conn, address= serveur_socket.accept()
    msg = ""
    data = ""

    while msg!= "exit" and msg!="bye" and data!= "exit" and data!="bye":
        data=conn.recv(1024).decode()
        print(data)
        msg=input("serveur -->")
        conn.send(msg.encode())

    conn.close
    rep=input("continuer (y/n):")
    if rep =='n':
        break
serveur_socket.close()