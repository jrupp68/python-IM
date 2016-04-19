from socket import*

serverPort = 12009
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
print("Ready to receive")

while 1:
        # incoming connection
        connectionSocket, addr = serverSocket.accept()

        # incoming message
        incoming1 = connectionSocket.recv(1024).decode('ascii')

        # get request out of incoming message
        request = incoming1.split("\t")[0].strip()

        outgoing = ""
        # check request and perform if found
        if(request == "GET_FRIENDS"):
                user = incoming1.split("\t")[1].strip()
                filename = user+"_FRIENDS.txt"
                file = open(filename, 'r')
                for line in file:
                        outgoing += line.split("\t")[0].strip() + "\t\t" + line.split("\t")[1].strip() + "\n"
                connectionSocket.send(outgoing.encode())

        elif(request == "GET_OFFLINE_MESSAGES"):
                user = incoming1.split("\t")[1].strip()
                filename = user+"_OFFLINE_MESSAGES"
                file = open(filename, 'r')

        elif(request == "GET_NEW_MESSAGES"):
                user = incoming1.split("\t")[1].strip()
                friend = incoming1.split("\t")[2].strip()
                filename = user+"_NEW_MESSAGES_FROM_"+friend
                file = open(filename, 'r')

        elif(request == "SEND_MESSAGE"):
                user = incoming1.split("\t")[1].strip()
                friend = incoming1.split("\t")[3]
                message = incoming1.split("\t")[2]

        elif(request == "ADD_FRIEND"):
                user = incoming1.split("\t")[1].strip()
                friend = incoming1.split("\t")[2]
                # check registration to see if the friend exists
                # if friend exists add friend to users friends list txt file
                # respond success and new friends list with status
                
                
