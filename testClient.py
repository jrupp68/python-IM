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

def register():
    username = input("Username :")
    password = input("Password :")
    passwordCheck = input("Password :")
    firstName = input("First Name :")
    lastName = input("Last Name :")
    email = input("Email :")

    outgoing = "REGISTER\t" + username + "\t" + password + "\t" + passwordCheck + "\t" + firstName + "\t" + lastName + "\t" + email
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))

    #If register is success then go to login page
    #If register fails then prompt user to re register

def login():
    username = input("Username :")
    password = input("Password :")

    outgoing = "LOGIN\t" + username + "\t" + password
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))

    #If login is success then open window with user friends list
    #If login fails, display why and prompt user to try again
    
def getFriends():
    outgoing = "GET_FRIENDS\tJRUPP68"
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print("Friends \t Status")
    print(incoming.decode('ascii'))

def addFriend():
    friend = input("Please enter the username of the friend you would like to add :")
    outgoing = "ADD_FRIEND\tjeff\t" + friend

    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))
        
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

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))


action = input("Enter \n1 - show friends list \n2 - send message \n3 - register \n4 - login \n5- Add Friend \n:")
print(action)
if(action == "1"):
    print("\n")
    getFriends()
elif(action == "2"):
    print('\n')
    sendMessage()
elif(action == "3"):
    print('\n')
    register()
elif(action == "4"):
    print("\n")
    login()
elif(action == "5"):
    print("\n")
    addFriend()


