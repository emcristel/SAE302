import socket

socket_client = socket.socket()
socket_client.connect(("localhost", 10000))
print("Connexion établie...")

msg = ""
data = ""

while msg!= "exit" and msg!="bye" and data!= "exit" and data!="bye":
    msg=input('client -->')
    socket_client.send(msg.encode())
    data = socket_client.recv(1024).decode()
    print(data)
socket_client.close()