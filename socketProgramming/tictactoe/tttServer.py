# -*- coding: utf-8 -*-
"""
Created on Sat May  1 13:44:57 2021

@author:
    2016730040 Frederick
    2017 Reinalta Sugianto
"""

'''
library needed
'''
from time import sleep
import tkinter as tk
import socket
import threading


'''
variable & lists initializing
'''
server = None
clientList = []
nameList = []
clientName = " "
playerInfo = []


'''
GUI codes
'''
window = tk.Tk()
window.title("TicTacToe Game Server GUI")
window.geometry("300x400")

# Top frame includes Start & Stop Server Button
topFrame = tk.Frame(window)
lblGuide = tk.Label(topFrame, 
                    text="Server Control for TicTacToe", 
                    font="Calibri 13").pack(side=tk.TOP, anchor="center")
btnStart = tk.Button(topFrame, 
                     text="Start Server", 
                     bg='green', 
                     command=lambda : validate())
btnStart.pack(side=tk.LEFT, pady=(20, 0))
btnStop = tk.Button(topFrame, 
                    text="Stop Server", 
                    state=tk.DISABLED, 
                    command=lambda : stopServer())
btnStop.pack(side=tk.LEFT, pady=(20, 0))
btnClose = tk.Button(master=topFrame, 
                     text="Close Server", 
                     command=window.destroy, bg='red')
btnClose.pack(side=tk.LEFT, pady=(20, 0))
topFrame.pack(side=tk.TOP, pady=(15, 0))

# Middle frame includes labels & textbox to insert address & port number
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Insert Address").grid(row=0)
txtAddr = tk.Entry(middleFrame)
txtAddr.grid(row=0, column=1)
lblPort = tk.Label(middleFrame, text = "Insert Port").grid(row=1)
txtPort = tk.Entry(middleFrame)
txtPort.grid(row=1, column=1)
#lblNotif = tk.Label(middleFrame, 
#                    text = "Insert Field -> press Validate").grid(row=2)
#btnValid = tk.Button(master=middleFrame, 
#                     text="Validate Address & Port", 
#                     command=lambda : validateInput(lblNotif, txtPort))
#btnStop.grid(row=3)
middleFrame.pack(side=tk.TOP, pady=(10, 0))

# Bottom frame includes a textbox containing client list
bottomFrame = tk.Frame(window)
lblLine = tk.Label(bottomFrame, text="Connected Client Lists:").pack()
scrollBar = tk.Scrollbar(bottomFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
boxName = tk.Text(bottomFrame, height=15, width=25)
boxName.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))
scrollBar.config(command=boxName.yview)
boxName.config(yscrollcommand=scrollBar.set, 
               state="disabled", 
               background="white", 
               highlightbackground="grey")
bottomFrame.pack(side=tk.BOTTOM, pady=(10, 10))
#window.mainloop()

'''
functions & method needed
'''

# Validate function exception, to make sure port is not empty
def validate():
    try:
        tk.messagebox.showinfo("Info", 
                               "If Address Field empty, default address will be used")
        startServer()
    except ValueError:
        tk.messagebox.showerror("Empty Port", "Port Field Can't be Empty!")
    except OSError:
        tk.messagebox.showerror("Address/Port Not Valid", 
                                "The requested address/port is not valid in its context!")

# Start server function
def startServer():
    global server, hostAddr, hostPort # codes are fine without this 'global'
    
    # if both hostAddr & hostPort put outside the function, it will crash since
    # the Entry object was just created and it will return null bcs Entry object
    # still empty.
    hostAddr = txtAddr.get()
    hostPort = int(txtPort.get())
    
    # set hostAddr to default 'localhost' if empty
    if(hostAddr==""):
        hostAddr = 'localhost'
        txtAddr.insert(0, "localhost")
    else:
        hostAddr
    print(hostAddr)
    print(hostPort)
    txtAddr.config(state=tk.DISABLED)
    txtPort.config(state=tk.DISABLED)
    
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print(socket.AF_INET)
    #print(socket.SOCK_STREAM)

    server.bind((hostAddr, hostPort))
    
    # listening for client connection
    server.listen(5)  
    tk.messagebox.showinfo("Connected!", "Server has Started!")

    threading._start_new_thread(clientConnection, (server, " "))

# Stop server function
def stopServer():
    global server # again, codes are fine without this 'global'
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)

# Control minimum number of clients to connect so the game can be start
def clientConnection(server, y):
    while True:
        if len(clientList) < 2:
            client, addr = server.accept()
            clientList.append(client)

            # create new thread so connection won't interfere with server thread
            threading._start_new_thread(gameControl, (client, addr))

# Function to receive message from client & send that message to other clients
def gameControl(connection, client_ip_addr):
    global server, clientName, clientList
    
    # send welcome message to client
    clientName = connection.recv(2048).decode()

    # this if-else is for identifying newly connected clients, so they can start
    # initializing their info
    if len(clientList) < 2:
        connection.send("connected".encode())
    else:
        connection.send("connected1".encode())

    # adds client to nameList, then adds nameList to the name box
    nameList.append(clientName)
    addClient(nameList)

    if len(clientList) > 1:
        sleep(1)
        noughts = ["O", "X"]

        # send opponent name and noughts
        clientList[0].send(("name%" + 
                            nameList[1] + 
                            "%noughts%" + 
                            noughts[0]).encode())
        clientList[1].send(("name%" + 
                            nameList[0] + 
                            "%noughts%" + 
                            noughts[1]).encode())

    while True:
        # get opponent choice from received data
        data = connection.recv(4096).decode()
        if not data: break

        # send coordinates (x, y) to other player
        if data.startswith("%coord%"):
            # decides which client to send the data
            if connection == clientList[0]:
                clientList[1].send(data.encode())
            else:
                # sends data from client[1] to other client[0]
                clientList[0].send(data.encode())

    # get client index to remove client from nameList & clientList
    i = getIndex(clientList, connection)
    del nameList[i]
    del clientList[i]
    connection.close()
    
    # adds updated list to the name box
    addClient(nameList)

# Add or remove name list of connected clients to the box
def addClient(name_list):
    boxName.config(state=tk.NORMAL)
    boxName.delete('1.0', tk.END)

    for c in name_list:
        boxName.insert(tk.END, c+"\n")
    boxName.config(state=tk.DISABLED)

# Get index of current client in the list
def getIndex(clientList, wanted):
    i = 0
    for conn in clientList:
        if conn == wanted:
            break
        i += 1
    return i

# Render the GUI
window.mainloop()