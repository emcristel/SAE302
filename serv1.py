import socket

serveur_socket=socket.socket()
serveur_socket.bind(("localhost", 10001))
serveur_socket.listen(1)
print("Serveur démarré...")

while True:
    conn, address= serveur_socket.accept()
    msg = ""
    data = ""

    while msg!= "exit" and msg!="bye" and data!= "exit" and data!="bye":
        data=serveur_socket.recv(1024).decode()
        print(data)
        msg=input("serveur -->")
        conn.send(msg.encode())
    conn.closer
    rep=input("continuer (y/n):")
    if rep ==y:
        break
serveur_socket.close()