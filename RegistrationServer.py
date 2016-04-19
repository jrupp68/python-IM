#Server registration

from socket import*

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
        print(incoming1)
        #Get request out of incoming message
        request = incoming1.split("\t")[0].strip()

        outgoing = ""

        #Check request and perform action
        if(request == "REGISTER"):
            
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
                # Don't send message to Client here
                #connectionSocket.send(registerStatus.encode())

            elif(password != passwordCheck):
                registerStatus="RETYPE"
                registerMessage= "Registration Status: Passwords Do Not Match. Re-Enter Passwords"
                print(registerMessage)
                #connectionSocket.send(registerStatus.encode())

            else:
                for line in open("RegisterFile.txt",'r'):
                    print(line)
                    if(line != ""):
                        print(line)
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
                    output_file = open("ONLINE_STATUS.txt", 'a')
                    toWrite = userName + "\t" + "OFFLINE" + "\n"
                    output_file.write(toWrite);
                    output_file.close()
                    filename = userName+"_MESSAGES.txt"
                    output_file = open(filename, 'a')
                    output_file.close()
                    registerStatus= "SUCCESS"
                    registerMessage= "Register Status: Registration Was Successful"
                    #connectionSocket.send(registerStatus.encode())

            connectionSocket.send(registerStatus.encode())

        elif(request == "GET_FRIENDS"):
            user = incoming1.split("\t")[1].strip().upper()
            filename = user+"_FRIENDS.txt"
            file = open(filename, 'r')
            for line in file:
                outgoing += line.split("\t")[0].strip().upper()
                statusFile = open("ONLINE_STATUS.txt", 'r')
                for line2 in statusFile:
                    if(line2.split("\t")[0].strip().upper() == line.split("\t")[0].strip().upper()):
                        outgoing += "\t\t" + line2.split("\t")[1].strip().upper() + "\n"
                        break
            connectionSocket.send(outgoing.encode())
            file.close()

        elif(request == "GET_OFFLINE_MESSAGES"):
            user = incoming1.split("\t")[1].strip().upper()
            #Add code for offline messages
            
        elif(request == "GET_NEW_MESSAGES"):
            user = incoming1.split("\t")[1].strip().upper()
            friend = incoming1.split("\t")[2].strip().upper()
            #Add code for getting new messages

        elif(request == "SEND_MESSAGE"):
            user = incoming1.split("\t")[1].strip().upper()
            friend = incoming1.split("\t")[3].strip().upper()
            message = incoming1.split("\t")[2].strip()

            filename = friend + "_MESSAGES.txt"
            file = open(filename, 'a')
            writeMessage = message + "\t" + user + "\n"
            a = file.write(writeMessage)
            print(a)
            file.close()

            if(a > 1):
                outgoing = "SUCCESS"
            else:
                outgoing = "FAILED"

            connectionSocket.send(outgoing.encode())

        elif(request == "ADD_FRIEND"):
            username = incoming1.split("\t")[1].strip().upper()
            friend = incoming1.split("\t")[2].strip().upper()

            file = open("RegisterFile.txt", 'r')
            for line in file:
                friendCheck = line.split("\t")[0].strip().upper()
                if(friend == friendCheck):
                    file.close()
                    filename = username + "_FRIENDS.txt"
                    print(filename)
                    writeFile = open(filename, 'a')
                    a = writeFile.write(friend+'\n')
                    print(a)
                    print(friend)
                    writeFile.close()
                    outgoing = "SUCCESS"
                    break
                else:
                    outgoing = "FAILED"

            file.close()
            connectionSocket.send(outgoing.encode())


            # respond success and new friends list with status

        elif(request == "LOGIN"):
            username = incoming1.split("\t")[1].strip().upper()

            password = incoming1.split("\t")[2].strip().upper()

            file = open("RegisterFile.txt", 'r')
            for line in file:
                usernameCheck = line.split("\t")[0].strip().upper()

                if(username == usernameCheck):
                    passwordCheck = line.split("\t")[1].strip().upper()

                    if(password == passwordCheck):
                        outgoing = "SUCCESS"
                        file = open("ONLINE_STATUS.txt", 'r')
                        filedata = file.read()
                        file.close

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

        elif(request == "VIEW_ALL_MESSAGES"):
            user = incoming1.split("\t")[1].strip().upper()

            filename = user + "_MESSAGES.txt"
            file = open(filename, 'r')
            outgoing = ""
            for line in file:
                outgoing += line.split("\t")[1].strip().upper() + ": " + line.split("\t")[0].strip()
            file.close()
            connectionSocket.send(outgoing.encode())

        elif(request == "LOGOUT"):
            #add online_status chagne to offline here
            user = incoming1.split("\t")[1].strip().upper()
            connectionSocket.close()
        else:
            print("Invalid Request")

connectionSocket.close()
        
