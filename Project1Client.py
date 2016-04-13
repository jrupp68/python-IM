from tkinter import*
from socket import*
#import smtplib for the actual sending function
import smtplib
#Import the email modules we need
from email.mime.text import MIMEText

def Home():
    root = Tk()
    root.title("IM Service")
    root.minsize(width=190,height=30)
    register = Button(root,text="Register",command=Register)
    register.grid(row=0,column=1)
    login = Button(root,text="Login",command=Login)
    login.grid(row=0,column=2)
    stop = Button(root,text="Exit",command=Exit)
    stop.grid(row=0,column=3)

def Register():
    root.withdraw()
    global new
    new = Tk()
    new.title("Register for Account")
    #the following is GUI code, variables explain the purpose
    name = Label(new,text="Username:")
    name.grid(row=0)
    nameEntry = Entry(new)
    nameEntry.grid(row=0,column=1)
    
    password = Label(new,text="Password:")
    password.grid(row=1)
    passwordEntry = Entry(new)
    passwordEntry.grid(row=1,column=1)
    
    REpassword = Label(new,text="Retype Password:")
    REpassword.grid(row=1)
    REpasswordEntry = Entry(new)
    REpasswordEntry.grid(row=2,column=1)
    
    fn = Label(new,text="First Name:")
    fn.grid(row=2)
    fnEntry = Entry(new)
    fnEntry.grid(row=2,column=1)
    
    ln = Label(new,text="Last Name:")
    ln.grid(row=3)
    lnEntry = Entry(new)
    lnEntry.grid(row=3,column=1)
    
    email = Label(new,text="Email:")
    email.grid(row=4)
    emailEntry = Entry(new)
    emailEntry.grid(row=4,column=1)
    
    #Submit Information Button, once pressed info will be sent to server
    submit = Button(new,text="Submit",command = sendInfo)
    submit.grid(row=5,column=1)

def sendInfo():
    #Server Connection Code
    serverName = "192.168.1.23" #Home Test Machine
    serverPort=12009
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    #Send information for Registration Validation
    clientSocket.send(nameEntry.encode())
    clientSocket.send(passwordEntry.encode())
    clientSocket.send(REpasswordEntry.encode())
    clientSocket.send(fnEntry.encode())
    clientSocket.send(lnEntry.encode())
    clientSocket.send(emailEntry.encode())

    #Wait for server response
    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))
    connectionSocket.close() #Close connection socket
    

def Login():
    root.withdraw()
    global login
    login = Tk()
    login.title("Register for Account")
    #the following is GUI code, variables explain the purpose
    name = Label(login,text="Username:")
    name.grid(row=0)
    nameEntry = Entry(login)
    nameEntry.grid(row=0,column=1)
    
    password = Label(login,text="Password:")
    password.grid(row=1)
    passwordEntry = Entry(login)
    passwordEntry.grid(row=1,column=1)    

    submit = Button(login,text="Login",command = sendLogin)
    submit.grid(row=5,column=0)

    forgot = Button(login,text="Forgot Password?",command = forgotPass)
    forgot.grid(row=5,column=1)

def sendLogin():
    #Server Connection Code
    serverName = "192.168.1.23" #Home Test Machine
    serverPort=12009
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    #Send information for Registration Validation
    clientSocket.send(nameEntry.encode())
    clientSocket.send(passwordEntry.encode())

    #Wait for server response
    incoming = clientSocket.recv(1024)
    print(incoming.decode('ascii'))
    connectionSocket.close() #Close connection socket
    
def Exit():
    root.destroy()

def forgotPass():
    with open("password.txt") as fp:
        #Create a text/plain message
        msg = MIMEText(fp.read())
            
    msg['Subject'] = 'Forgotten Password'
    msg['From'] = motorider9911@gmail.com
    msg['To'] = gjones8580@live.com

    #Send the message via our own SMTP server
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
    
    global passRecover
    passRecover = Tk()
    passRecover.title("Recover Forgotten Password")
    passSent = Label(passRecover, text="Your Password has been sent to your email address")
    passSent.grid(row=0)
    home = Button(passRecover,text="Home",command = Home)
    home.grid(row=1)

root = Tk()
root.title("IM Service")
root.minsize(width=190,height=30)
register = Button(root,text="Register",command=Register)
register.grid(row=0,column=1)
login = Button(root,text="Login",command=Login)
login.grid(row=0,column=2)
stop = Button(root,text="Exit",command=Exit)
stop.grid(row=0,column=3)

root.mainloop()

