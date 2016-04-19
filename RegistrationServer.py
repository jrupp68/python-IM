#Server registration

from socket import*

serverPort = 12009
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(10)
print("Ready")

while 1:
    connectionSocket, address = serverSocket.accept()

    #Wait for incoming message
    incoming1 = connectionSocket.recv(1024).decode('ascii')

    #Get request out of incoming message
    request = incoming1.split("\t")[0].strip()

    outgoing = ""

    #Check request and perform action
    if(request == "REGISTER"):
        
        register = incoming1+"\n"

        #split the the data received into variables
        userName= register.split("\t")[1].strip()
        password= register.split("\t")[2].strip()
        passwordCheck= register.split("\t")[3].strip()
        firstName= register.split("\t")[4].strip()
        lastName= register.split("\t")[5].strip()
        email= register.split("\t")[6].strip()
        registerStatus = "GOOD"
        
        #Check if the length of password not <6
        if(len(password)<6):
            registerStatus="SHORT"
            registerMessage= "Registration Status: Password Too Short"
            print(registerMessage)
            # Don't send message to Client here
            #connectionSocket.send(registerStatus.encode())

        elif(password != passwordCheck):
            registerStatus="RETYPE"
            registerMessage= "Registration Status: Passwords Do Not Match. Re-Enter Passwords"
            print(registerMessage)
            #connectionSocket.send(registerStatus.encode())

        else:
            for line in open("RegisterFile.txt",'r'):
                if(line != ""):
                    print(line)
                    registeredID= line.split("\t")[0].strip()
                    regFirstName= line.split("\t")[2].strip()
                    regLastName= line.split("\t")[3].strip()

                    #Check if the userName/userID is already registered.
                    if(userName == registeredID):
                        #If registered check with First Name and Last
                        if(regFirstName == firstName and regLastName == lastName):
                            registerStatus = "EXIST"
                            registerMessage= "Register Status: You Are Already Registered"
                            print(registerMessage)
                            #connectionSocket.send(registerStatus.encode())
                        else:
                            registerStatus= "TAKEN"
                            registerMessage= "Register Status: User Name Unavailable"
                            print(registerMessage)
                            #connectionSocket.send(registerStatus.encode())
            #If everything is correct, Register
            if(registerStatus == "GOOD"):
                forRegister = userName+"\t"+password+"\t"+firstName+"\t"+lastName+"\t"+email+"\n"
                output_file= open("RegisterFile.txt", 'a')
                output_file.write(forRegister)
                output_file.close()
                filename = userName+"_FRIENDS.txt"
                output_file = open(filename, 'a')
                output_file.close()
                registerStatus= "SUCCESS"
                registerMessage= "Register Status: Registration Was Successful"
                #connectionSocket.send(registerStatus.encode())

        connectionSocket.send(registerStatus.encode())

    elif(request == "GET_FRIENDS"):
        user = incoming1.split("\t")[1].strip()
        filename = user+"_FRIENDS.txt"
        file = open(filename, 'r')
        for line in file:
            outgoing += line.split("\t")[0].strip() + "\t\t" + line.split("\t")[1].strip() + "\n"
        connectionSocket.send(outgoing.encode())
        file.close()

    elif(request == "GET_OFFLINE_MESSAGES"):
        user = incoming1.split("\t")[1].strip()
        #Add code for offline messages
        
    elif(request == "GET_NEW_MESSAGES"):
        user = incoming1.split("\t")[1].strip()
        friend = incoming1.split("\t")[2].strip()
        #Add code for getting new messages

    elif(request == "SEND_MESSAGE"):
        user = incoming1.split("\t")[1].strip()
        friend = incoming1.split("\t")[3]
        message = incoming1.split("\t")[2]

    elif(request == "ADD_FRIEND"):
        username = incoming1.split("\t")[1].strip()
        friend = incoming1.split("\t")[2].strip()

        file = open("RegisterFile.txt", 'r')
        for line in file:
            friendCheck = line.split("\t")[0].strip()
            if(friend == friendCheck):
                filename = username + "_FRIENDS.txt"
                writeFile = open(filename, 'a')
                writeFile.write(friend)
                print(friend)
                writeFile.close
                outgoing = "SUCCESS"

        file.close()
        connectionSocket.send(outgoing.encode())


        # respond success and new friends list with status

    elif(request == "LOGIN"):
        username = incoming1.split("\t")[1].strip()
        print(username)
        password = incoming1.split("\t")[2].strip()
        print(password)
        file = open("RegisterFile.txt", 'r')
        for line in file:
            usernameCheck = line.split("\t")[0].strip()
            print(usernameCheck)
            if(username == usernameCheck):
                passwordCheck = line.split("\t")[1].strip()
                print(password)
                if(password == passwordCheck):
                    outgoing = "SUCCESS"
                else:
                    outgoing = "WRONG_PASSWORD"
            else:
                outgoing = "BAD_USERNAME"
        file.close()
        connectionSocket.send(outgoing.encode())
        
    else:
        print("Invalid Request")

connectionSocket.close()
        
