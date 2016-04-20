#Server registration

# After login, GUI should show friends list with current online status and
# if there are any new/undelivered messages

# To send a message to a friend (either offline or online) you click on the
# button for that specific friend. Clicking that button opens a chat (not sure
# if this should be in a new window or the same window) where it displays all
# messages that have been sent between

import os
from socket import*

def register(incoming1):

    register = incoming1+"\n"

    #split the the data received into variables
    userName= register.split("\t")[1].strip().upper()
    password= register.split("\t")[2].strip().upper()
    passwordCheck= register.split("\t")[3].strip().upper()
    firstName= register.split("\t")[4].strip().upper()
    lastName= register.split("\t")[5].strip().upper()
    email= register.split("\t")[6].strip().upper()
    registerStatus = "GOOD"
    
    #Check if the length of password not <6
    if(len(password)<6):
        registerStatus="SHORT"
        registerMessage= "Registration Status: Password Too Short"
        print(registerMessage)

    elif(password != passwordCheck):
        registerStatus="RETYPE"
        registerMessage= "Registration Status: Passwords Do Not Match. Re-Enter Passwords"
        print(registerMessage)

    else:
        for line in open("RegisterFile.txt",'r'):
            if(line != ""):
                registeredID= line.split("\t")[0].strip().upper()
                regFirstName= line.split("\t")[2].strip().upper()
                regLastName= line.split("\t")[3].strip().upper()

                #Check if the userName/userID is already registered.
                if(userName == registeredID):
                    #If registered check with First Name and Last
                    if(regFirstName == firstName and regLastName == lastName):
                        registerStatus = "EXIST"
                        registerMessage= "Register Status: You Are Already Registered"
                        print(registerMessage)

                    else:
                        registerStatus= "TAKEN"
                        registerMessage= "Register Status: User Name Unavailable"
                        print(registerMessage)

        #If everything is correct, Register
        if(registerStatus == "GOOD"):
            forRegister = userName+"\t"+password+"\t"+firstName+"\t"+lastName+"\t"+email+"\n"
            output_file= open("RegisterFile.txt", 'a')
            output_file.write(forRegister)
            output_file.close()
            filename = userName+"_FRIENDS.txt"
            output_file = open(filename, 'a')
            output_file.close()
            output_file = open("ONLINE_STATUS.txt", 'a')
            toWrite = userName + "\t" + "OFFLINE" + "\n"
            output_file.write(toWrite);
            output_file.close()
            filename = userName+"_MESSAGES.txt"
            output_file = open(filename, 'a')
            output_file.close()
            registerStatus= "SUCCESS"
            registerMessage= "Register Status: Registration Was Successful"

    connectionSocket.send(registerStatus.encode())

def login(incoming1):
    # Get username and password from request
    username = incoming1.split("\t")[1].strip().upper()
    password = incoming1.split("\t")[2].strip().upper()

    file = open("RegisterFile.txt", 'r')

    # Find user in registration text file and check credentials
    for line in file:
        usernameCheck = line.split("\t")[0].strip().upper()

        # User found, check password
        if(username == usernameCheck):

            # Get password from registration file
            passwordCheck = line.split("\t")[1].strip().upper()

            # Passwords are equal, send success message and change status to online
            if(password == passwordCheck):
                outgoing = "SUCCESS"
                file = open("ONLINE_STATUS.txt", 'r')

                # Get data in online status text file
                filedata = file.read()
                file.close()

                # Replace OFFLINE with ONLINE for newly logged in user
                newdata = filedata.replace(username + "\t" + "OFFLINE", username + "\t" + "ONLINE")
                file = open("ONLINE_STATUS.txt", 'w')
                file.write(newdata)
                file.close()
                break            
            else:
                outgoing = "WRONG_PASSWORD"
        else:
            outgoing = "BAD_USERNAME"
    file.close()
    connectionSocket.send(outgoing.encode())

def getFriendsList(incoming1):
    outgoing = ""

    # Get username
    user = incoming1.split("\t")[1].strip().upper()

    # Check if user is logged in
    status = checkLogin(user)

    if(status == "ONLINE"):
        filename = user+"_FRIENDS.txt"

        # Open user's friendslist text file
        file = open(filename, 'r')

        # Chec if the file is empty
        if os.stat(filename).st_size>0:
            for line in file:

                # Get each user from friendslist 
                outgoing += line.split("\t")[0].strip().upper()

                # Open online status text file
                statusFile = open("ONLINE_STATUS.txt", 'r')
                for line2 in statusFile:

                    # Find friend in online status text file
                    if(line2.split("\t")[0].strip().upper() == line.split("\t")[0].strip().upper()):

                        # Friend found, get online status
                        outgoing += "\t\t" + line2.split("\t")[1].strip().upper() + "\n"
                        statusFile.close()
                        break

            connectionSocket.send(outgoing.encode())
            file.close()
        else:
            file.close()
            print("The file is empty")
            outgoing = "Your friends list is empty"
            connectionSocket.send(outgoing.encode())
    else:
        outgoing = "You are not logged in, please login to continue"
    
    # Send list of friends and their online status'
    connectionSocket.send(outgoing.encode())

def addFriend(incoming1):
    # Get user and friend username from request
    username = incoming1.split("\t")[1].strip().upper()
    friend = incoming1.split("\t")[2].strip().upper()

    # Check if user is logged on
    status = checkLogin(username)

    if(status == "ONLINE"):
        file = open("RegisterFile.txt", 'r')

        # Check to make sure friend exists in registration file
        for line in file:
            friendCheck = line.split("\t")[0].strip().upper()

            # Friend found, add them to user's friendslist
            if(friend == friendCheck):
                file.close()
                filename = username + "_FRIENDS.txt"
                writeFile = open(filename, 'a')
                writeFile.write(friend+'\n')
                writeFile.close()
                outgoing = "SUCCESS"
                break
            else:
                outgoing = "FAILED"

        file.close()
    else:
        outgoing = "You are not logged in, please login to continue"

    connectionSocket.send(outgoing.encode())

    # respond success and new(updated) friends list with status

def sendMessage(incoming1):
    # Get information from request
    user = incoming1.split("\t")[1].strip().upper()
    friend = incoming1.split("\t")[3].strip().upper()
    message = incoming1.split("\t")[2].strip()

    # Check if user is logged on
    status = checkLogin(user)
    if(status == "ONLINE"):
        friendStatus = checkIfFriend(user, friend)
        if(friendStatus == "1"):
            filename = friend + "_MESSAGES.txt"

            # Open friends message text file
            file = open(filename, 'a')
            writeMessage = message + "\t" + user + "\t" + "1" + "\n"

            # Write message to text file
            a = file.write(writeMessage)
            file.close()

            # Check to make sure message was written
            if(a > 1):
                outgoing = "SUCCESS"

            else:
                outgoing = "FAILED"
        else:
            outgoing = "Friend not found"
    else:
        outgoing = "You are not logged in, please login to continue"
        
    connectionSocket.send(outgoing.encode())

    
def checkNewMessages(incoming1):
    # Get user from request
    user = incoming1.split("\t")[1].strip().upper()

    filename = user + "_MESSAGES.txt"
    file = open(filename, 'r')
    outgoing = ""
    
    for line in file:
        if(line != ""):
            # Check if there are any '1's in the users message file
            if(line.split("\t")[2].strip() == "1"):
                # Add user who sent new message
                if(outgoing == ""):
                    outgoing += "New messages from these users:" + "\n" + line.split("\t")[1].strip() + "\n"

    file.close()

    if(outgoing == ""):
        outgoing = "No new messages"
        
    connectionSocket.send(outgoing.encode())
        
def viewMessages(incoming1):
    # Get user from request
    user = incoming1.split("\t")[1].strip().upper()
    sender = incoming1.split("\t")[2].strip().upper()
                            
    # Check if user is logged on
    status = checkLogin(user)

    if(status == "ONLINE"):
        # Open users messages text file
        filename = user + "_MESSAGES.txt"
        file = open(filename, 'r')

        outgoing = ""
        # Write all messages to a string
        for line in file:
            outgoing += line.split("\t")[1].strip().upper() + ": " + line.split("\t")[0].strip() + "\n"
        file.close()

        # Replace all 1's in users message text file to 0's (1 = new message, 0 = read message)
        file = open(filename, 'r')
        filedata = file.read()
        file.close()

        newdata = filedata.replace(sender + "\t" + "1", sender + "\t" + "0")

        file = open(filename, 'w')
        file.write(newdata)
        file.close()

    else:
        outoing = "You are not logged in, please login to continue"

    # Send string containing messges
    connectionSocket.send(outgoing.encode())

def logout(incoming1):
    # Get user from request
    username = incoming1.split("\t")[1].strip().upper()

    # Open online status text file
    file = open("ONLINE_STATUS.txt", 'r')

    # Get data in online status text file
    filedata = file.read()
    file.close()

    # Replace ONLINE with OFFLINE for newly logged in user
    newdata = filedata.replace(username + "\t" + "ONLINE", username + "\t" + "OFFLINE")
    file = open("ONLINE_STATUS.txt", 'w')
    file.write(newdata)
    file.close()

    outgoing = "LOGGED_OFF"
    connectionSocket.send(outgoing.encode())    

def checkLogin(user):
    # Open online status text file to check if user is logged on
    file = open("ONLINE_STATUS.txt", 'r')

    for line in file:
        userCheck = line.split("\t")[0].strip().upper()

        # If user if found check online status
        if(user == userCheck):
            userStatus = line.split("\t")[1].strip().upper()

            # If status is online, return ONLINE
            if(userStatus == "ONLINE"):
               return "ONLINE"
            else:
               return "OFFLINE"

    # User not found, return offline        
    return "OFFLINE"

def checkIfFriend(user, friend):
    filename = user + "_FRIENDS.txt"
    file = open(filename, 'r')

    for line in file:
        friendCheck = line.split("\n")[0].strip().upper()
        if(friend == friendCheck):
            file.close()
            return "1"
    file.close()
    return "0"
        
serverPort = 12009
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(10)
print("Ready")

while 1:
    connectionSocket, address = serverSocket.accept()

    while 1:
        #Wait for incoming message
        incoming1 = connectionSocket.recv(1024).decode('ascii')

        #Get request out of incoming message
        request = incoming1.split("\t")[0].strip()

        #Check request and perform action
        if(request == "REGISTER"):
            register(incoming1)
            
        elif(request == "LOGIN"):            
           login(incoming1)
           
        elif(request == "GET_FRIENDS"):
            getFriendsList(incoming1)
            
        elif(request == "ADD_FRIEND"):
            addFriend(incoming1)
            
        elif(request == "SEND_MESSAGE"):
            sendMessage(incoming1)

        elif(request == "VIEW_MESSAGES"):
            viewMessages(incoming1)

        elif(request == "CHECK_NEW_MESSAGES"):
            checkNewMessages(incoming1)
            
        elif(request == "LOGOUT"):
            logout(incoming1)

        else:
            print("Invalid Request")

connectionSocket.close()
        
