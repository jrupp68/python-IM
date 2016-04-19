from tkinter import*
from socket import*

# root = Tk()
# root.title("IM Service")
# root.minsize(width=300,height=300)

# im = Message(root, text="Test Message", width=200)
# im.grid(row=0, column=1)
# im.pack

# msgLabel = Label(root, text="Message :")
# msgLabel.grid(row = 5, column = 0)

# msg = Entry(root)
# msg.grid(row = 5, column = 1)

# send = Button(root, text="Send")
# send.grid(row = 5, column = 2)
#friend1 = Button(root,text="Jeff")
#friend1.grid(row=0)
#friend2 = Button(root,text="Adam")
#friend2.grid(row=1)
#friend3 = Button(root,text="John")
#friend3.grid(row=2)

# root.mainloop()

serverName = "localhost"
serverPort = 12009
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def getFriends():
	outgoing = "GET_FRIENDS\tJRUPP68"
	clientSocket.send(outgoing.encode())

	incoming = clientSocket.recv(1024)
	print("Friends \t Status")
	print(incoming.decode('ascii'))

def addFriend():
        friend = input("Please enter the username of the friend you would like to add :")
        outgoing = "ADD_FRIEND\tJRUPP68" + friend

        clientSocket.send(outgoing.encode())
        
def getOfflineMessages():
	outgoing = "GET_OFFLINE_MESSAGES \t JRUPP68"
	clientSocket.send(outgoing.encode())

	incoming = clientSocket.recv(1024)
	print(incoming.decode('ascii'))

def getNewMessages():
	outgoing = "GET_NEW_MESSAGES \t JRUPP68"
	clientSocket.send(outgoing.encode())

	incoming = clientSocket.recv(1024)
	print(incoming.decode('ascii'))

def sendMessage():
        print("Please enter username of the friend you want to message :")
        user = input()
        print("Enter the message :")
        message = input()
        print("Please enter your username :")
        me = input()
        outgoing = "SEND_MESSAGE \t " + me + "\t" + message + "\t" + user
        clientSocket.send(outgoing.encode())


action = input("Enter 1 to show friends list \nEnter 2 to send message :")
print(action)
if(action == "1"):
        print("\n")
        getFriends()
elif(action == "2"):
        print("Message")
        sendMessage()


