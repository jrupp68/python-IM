from socket import*

serverName = "localhost"
serverPort = 12009
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def register(username, password, passwordCheck, firstName, lastName, email):
    outgoing = "REGISTER\t" + username + "\t" + password + "\t" + passwordCheck + "\t" + firstName + "\t" + lastName + "\t" + email
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))

    #If register is success then go to login page
    #If register fails then prompt user to re register

def login(username, password):
    outgoing = "LOGIN\t" + username + "\t" + password
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))

    #If login is success then open window with user friends list
    #If login fails, display why and prompt user to try again
    
def getFriends(username):
    outgoing = "GET_FRIENDS\t" + user
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print("Friends \t Status")
    print(incoming.decode('ascii'))

def addFriend(user, friend):
    outgoing = "ADD_FRIEND\t" + user + "\t" + friend
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))

def sendMessage(sender, receiver, message):
    outgoing = "SEND_MESSAGE \t " + sender + "\t" + message + "\t" + receiver
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))

def viewMessages(user, friend):
    outgoing = "VIEW_MESSAGES\t" + user + "\t" + friend
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))

def checkMessages(user):
    outgoing = "CHECK_NEW_MESSAGES\t" + user
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))

def logout(user):
    outgoing = "LOGOUT\t" + user
    clientSocket.send(outgoing.encode())

    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))

while 1:
    action = input("Enter \n1 - Show Friends List \n2 - Send Message \n3 - Register \n4 - Login \n5 - Add Friend \n6 - View Messages \n7 - Check For New Messages \n8 - Logout \n:")
    print(action)
    if(action == "1"):
        print("\n")
        user = input("Please enter your username :")
        
        getFriends(user)
    elif(action == "2"):
        print('\n')
        print("Please enter username of the friend you want to message :")
        receiver = input()
        print("Enter the message :")
        message = input()
        print("Please enter your username :")
        sender = input()
        
        sendMessage(sender, receiver, message)
    elif(action == "3"):
        print('\n')
        username = input("Username :")
        password = input("Password :")
        passwordCheck = input("Password :")
        firstName = input("First Name :")
        lastName = input("Last Name :")
        email = input("Email :")
        
        register(username, password, passwordCheck, firstName, lastName, email)
    elif(action == "4"):
        print("\n")
        username = input("Username :")
        password = input("Password :")
        
        login(username, password)
    elif(action == "5"):
        print("\n")
        friend = input("Please enter the username of the friend you would like to add :")
        user = input("Please enter your username :")
        
        addFriend(user, friend)
    elif(action == "6"):
        print("\n")
        user = input("Please enter your username :")
        friend = input("Please enter friend username of messsages you want to veiw :")
        
        viewMessages(user, friend)
    elif(action == "7"):
        print("\n")
        user = input("Pleae enter your username :")

        checkMessages(user)
    elif(action == "8"):
        print("\n")
        user = input("Please enter your username :")

        logout(user)