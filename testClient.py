from tkinter import*
from socket import*

root = Tk()
root.title("IM Service")
root.minsize(width=300,height=300)

im = Message(root, text="Test Message", width=200)
im.grid(row=0, column=1)
im.pack

msgLabel = Label(root, text="Message :")
msgLabel.grid(row = 5, column = 0)

msg = Entry(root)
msg.grid(row = 5, column = 1)

send = Button(root, text="Send")
send.grid(row = 5, column = 2)
#friend1 = Button(root,text="Jeff")
#friend1.grid(row=0)
#friend2 = Button(root,text="Adam")
#friend2.grid(row=1)
#friend3 = Button(root,text="John")
#friend3.grid(row=2)

root.mainloop()
