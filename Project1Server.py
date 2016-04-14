from socket import*

serverPort = 12009
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
print("Ready to receive")

while 1:
    connectionSocket, addr = serverSocket.accept()

    incoming1 = connectionSocket.recv(1024)

    if(incoming1.decode('ascii').upper() == "SENDMSG"):
        outgoing1 = "SENDMSG"
        connectionSocket.send(outgoing1.encode())
