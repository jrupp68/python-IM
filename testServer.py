from socket import*

serverPort = 12009
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
print("Ready to receive")

while 1:
	connectionSocket, addr = serverSocket.accept()

	incoming1 = connectionSocket.recv(1024).decode('ascii')
	
	request = incoming1.split("\t")[0].strip()
	user = incoming1.split("\t")[1].strip()

	if(request == "GET_FRIENDS"):
		filename = user+"_FRIENDS"
		file = open(filename, r)
		for line in file:
			outgoing += line.split("\t")[0].strip() + line.split("\t")[1].strip() + "\n"
		connectionSocket.send(outgoing.encode())

	elif(request == "GET_OFFLINE_MESSAGES"):
		filename = user+"_OFFLINE_MESSAGES"
		file = open(filename, r)

	elif(request == "GET_NEW_MESSAGES"):
		friend = incoming1.split("\t")[2].strip()
		filename = user+"_NEW_MESSAGES_FROM_"+friend
		file = open(filename, r)