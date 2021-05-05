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
from tkinter import PhotoImage
from tkinter.ttk import *

from time import sleep
import tkinter as tk
import socket
import threading


'''
variable & lists initializing
'''
client = None
hostAddr = "localhost"
hostPort = 7777

# number column of tictactoe made
colNumber = 3
labelList = []
myTurn = False
iStart = False

playerInfo = {
    "name": "eric",
    "symbol": "X",
    "color" : "",
    "score" : 0
}

player2Info = {
    "name": "rein",
    "symbol": "O",
    "color": "",
    "score": 0
}


'''
GUI codes
'''
window = tk.Tk()
window.title("TicTacToe Game Client GUI")
window.geometry("300x250")

# Registration Frame, which connects client to the server requiring to fill a
# names. It includes a label and an entry for name, address & port number, and
# acts as parent of all frame
regisFrame = tk.Frame(window)
regisFrame.pack()

# Top frame includes just title of the apps
topFrame = tk.Frame(regisFrame)
lblGuide = tk.Label(topFrame, 
                    text="Client Control for TicTacToe", 
                    font="Calibri 13").pack(side=tk.TOP, anchor="center")
topFrame.pack(side=tk.TOP)

# Btn frame includes all the button for the apps
btnFrame = tk.Frame(regisFrame)
btnStart = tk.Button(topFrame, 
                     text="Start Connection", 
                     bg='green', 
                     command=lambda : validate())
btnStart.pack(side=tk.LEFT, pady=(20, 0))
btnClose = tk.Button(master=topFrame, 
                     text="Cancel Connection", 
                     command=window.destroy, bg='red')
btnClose.pack(side=tk.LEFT, padx=(5, 0),pady=(20, 0))
btnFrame.pack(side=tk.TOP)

# Name frame includes label & entry to insert name
nameFrame = tk.Frame(regisFrame)
lblName = tk.Label(nameFrame, text = "Write your Name:").pack(side=tk.LEFT)
txtName = tk.Entry(nameFrame)
txtName.pack(side=tk.LEFT)
nameFrame.pack(side=tk.TOP, pady=(10, 0))

# Addr frame includes label & entry to insert address
addrFrame = tk.Frame(regisFrame)
lblHost = tk.Label(addrFrame, text = "Insert Address").pack(side=tk.LEFT)
txtAddr = tk.Entry(addrFrame)
txtAddr.pack(side=tk.LEFT)
addrFrame.pack(side=tk.TOP, pady=(10, 0))

# Addr frame includes label & entry to insert port
portFrame = tk.Frame(regisFrame)
lblPort = tk.Label(portFrame, text = "Insert Port").pack(side=tk.LEFT)
txtPort = tk.Entry(portFrame)
txtPort.pack(side=tk.LEFT)
portFrame.pack(side=tk.TOP, pady=(10, 0))
#window.mainloop()

# Main Game Frame, it will launched when Registration Frame has passed. It 
# includes a label for the board and for notification status
gameFrame = tk.Frame(window)

# creates notification bar
lblNotif = tk.Label(gameFrame, 
                      text="Status: Not connected to server", 
                      font="Calibri 14 bold")
lblNotif.grid(row=0, columnspan=3)

# creates the board (2 dimension needs 2 level of array)
for x in range(3):
    for y in range(3):
        lbl = tk.Label(gameFrame, 
                       text=" ", 
                       font="Verdana 20 bold", 
                       height=2, 
                       width=5)
        lbl.bind("<Button-1>", lambda e, xy=[x, y]: clickCalculate(xy))
        lbl.grid(row=(x+1), column=(y+1))

        sign = {"coord": [x, y], "symbol": "", "label": lbl, "ticked": False}
        labelList.append(sign)
#window.mainloop()

# delete previous 'registration' frame
gameFrame.pack_forget()


'''
functions & method needed
'''
# Validate names inserted & make sure port not empty, adds the name to a player 
# list, then launch method to connect to server
def validate():
    global playerInfo
    try:
        if len(txtName.get()) < 1:
            tk.messagebox.showerror(title="Check Names!", 
                                message="You MUST enter your first name!")
        else:
            tk.messagebox.showinfo("Info", 
                                   "If Address Field empty, default address will be used")
            playerInfo["name"] = txtName.get()
            startClient(txtName.get())
    except ValueError:
        tk.messagebox.showerror("Empty Port", "Port Field Can't be Empty!")
    except OSError:
        tk.messagebox.showerror("Address/Port Not Valid", 
                                "The requested address/port is not valid in its context!")

# Functions to start a connection to server, and run a new thread on 
# connectionControl method
def startClient(name):
    global client, hostPort, hostAddr
    try:
        # if both hostAddr & hostPort put outside the function, it will crash 
        # since the Entry object was just created and it will return null bcs 
        # Entry object still empty.
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
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((hostAddr, hostPort))
        
        # send the client name to server after connection successful
        client.send(name.encode())
        # start a new thread so client message in connectionControl won't 
        # interfere with the main connection thread
        threading._start_new_thread(connectionControl, (client, "m"))
        regisFrame.pack_forget()
        gameFrame.pack(side=tk.TOP)
        window.title("TicTacToe Client GUI for " + name)
    except ConnectionRefusedError:
        tk.messagebox.showerror(title="Connection Error!", 
                                message="Failed to create connection to host: " + 
                                hostAddr + 
                                " with port: " + 
                                str(hostPort) + 
                                " Please check address & port!")
    
# Functions to control an ongoing connection and message parsing to launch 
# specific instructions on gameplay and connection status
def connectionControl(socket, m):
    global playerInfo, player2Info, myTurn, iStart
    while True:
        message = socket.recv(2048).decode()

        if not message: break

        # this if is for the clients to start initializing their profile info
        if message.startswith("conn"):
            if message == "connected":
                playerInfo["color"] = "red"
                player2Info["color"] = "blue"
                lblNotif["text"] = "Welcome " + playerInfo["name"] + "! More player needed"
            elif message == "connected1":
                lblNotif["text"] = "Welcome " + playerInfo["name"] + "! Starting game..."
                playerInfo["color"] = "blue"
                player2Info["color"] = "red"
                
        # this if is for the clients to parse connection and set whose player 
        # will play first. we set X to run first
        elif message.startswith("name%"):
            temp = message.replace("name%", "")
            temp = temp.replace("%noughts%", "")
            name_index = temp.find("%")
            symbol_index = temp.rfind("%")
            player2Info["name"] = temp[0:name_index]
            playerInfo["symbol"] = temp[symbol_index:len(temp)]

            # set player symbol
            if playerInfo["symbol"] == "X":
                player2Info["symbol"] = "O"
            else:
                player2Info["symbol"] = "X"
            lblNotif["text"] = player2Info["name"] + " is connected!"
            sleep(3)
            
            # check whose turn to play
            if playerInfo["symbol"] == "X":
                lblNotif["text"] = "It's your turn!"
                myTurn = True
                iStart = True
            else:
                lblNotif["text"] = player2Info["name"] + "'s turn!"
                iStart = False
                myTurn = False
            
        # this if is for the client to set the board's coordinate, and adds the 
        # noughts to the list so it can be calculated
        elif message.startswith("%coord%"):
            temp = message.replace("%coord%", "")
            _x = temp[0:temp.find("%")]
            _y = temp[temp.find("%") + 1:len(temp)]

            # update board
            noughtsIndex = int(_x) * colNumber + int(_y)
            label = labelList[noughtsIndex]
            label["symbol"] = player2Info["symbol"]
            label["label"]["text"] = player2Info["symbol"]
            label["label"].config(foreground=player2Info["color"])
            label["ticked"] = True

            # check the coordinates to make sure winning status
            result = isWin()
            # opponent win
            if result[0] is True and result[1] != "":
                player2Info["score"] = player2Info["score"] + 1
                if result[1] == player2Info["symbol"]:  #
                    lblNotif["text"] = "Game over, You Lost! Your Score: " + str(playerInfo["score"]) + " - " \
                        "" + player2Info["name"] + "'s Score: " + str(player2Info["score"])
                    lblNotif.config(foreground="red")
                    threading._start_new_thread(initialize, ("", ""))
            # draw
            elif result[0] is True and result[1] == "":
                lblNotif["text"] = "Game over, Draw! Your Score: " + str(playerInfo["score"]) + " - " \
                    "" + player2Info["name"] + "'s Score: " + str(player2Info["score"])
                lblNotif.config(foreground="blue")
                threading._start_new_thread(initialize, ("", ""))
            # still playing
            else:
                myTurn = True
                lblNotif["text"] = "It's your turn!"
                lblNotif.config(foreground="black")
    socket.close()
#window.mainloop()

# Functions to initialize the game, and runs when a game is over or is about to
# start after successful 2 player parsing
def initialize(arg0, arg1):
    global labelList, myTurn, playerInfo, player2Info, iStart
    sleep(3)

    # clean and initialize the list from previous filling
    for i in range(len(labelList)):
        labelList[i]["symbol"] = ""
        labelList[i]["ticked"] = False
        labelList[i]["label"]["text"] = ""

    # create simple notification that indicates the game is starting
    lblNotif.config(foreground="black")
    lblNotif["text"] = "Game's starting."
    sleep(1)
    lblNotif["text"] = "Game's starting.."
    sleep(1)
    lblNotif["text"] = "Game's starting..."
    sleep(1)

    # check whose player's turn, then start the game
    if iStart:
        iStart = False
        myTurn = False
        lblNotif["text"] = player2Info["name"] + "'s turn!"
    else:
        iStart = True
        myTurn = True
        lblNotif["text"] = "Your turn!"

# Functions to calculate every click's coordinate in a label
def clickCalculate(xy):
    global client, myTurn
    # convert position to linear coordinate 
    noughtsIndex = xy[0] * colNumber + xy[1]
    label = labelList[noughtsIndex]
    if myTurn:
        if label["ticked"] is False:
            label["label"].config(foreground=playerInfo["color"])
            label["label"]["text"] = playerInfo["symbol"]
            label["ticked"] = True
            label["symbol"] = playerInfo["symbol"]
            # send coordinate to server, then switches turn
            client.send(("%coord%" + str(xy[0]) + "%" + str(xy[1])).encode())
            myTurn = False

            # check whether this new coordinates leads the game to a win or draw
            result = isWin()
            # if it leads to your winning
            if result[0] is True and result[1] != "":
                playerInfo["score"] = playerInfo["score"] + 1
                lblNotif["text"] = "Game over, You won! Your Score: " + str(playerInfo["score"]) + " - " \
                    "" + player2Info["name"] + "'s Score: " + str(player2Info["score"])
                lblNotif.config(foreground="green")
                threading._start_new_thread(initialize, ("", ""))
            # if it leads to a draw
            elif result[0] is True and result[1] == "":
                lblNotif["text"] = "Game over, Draw! Your Score: " + str(playerInfo["score"]) + " - " \
                    "" + player2Info["name"] + "'s Score: " + str(player2Info["score"])
                lblNotif.config(foreground="blue")
                threading._start_new_thread(initialize, ("", ""))
            # if it leads to nothing
            else:
                lblNotif["text"] = player2Info["name"] + "'s turn!"
    else:
        lblNotif["text"] = "Not your turn!"
        lblNotif.config(foreground="red")

# Function for checking win status, act as wrapper for all checking function
def isWin():
    # row noughts check
    result = rowCheck()
    if result[0]:
        return result

    # column noughts check
    result = colCheck()
    if result[0]:
        return result
    
    # diagonal noughts check
    result = diagCheck()
    if result[0]:
        return result
    
    # check whether both player won't win
    result = isDraw()
    return result

# Slave Function for checking board's grid, which will turn a 'draw' if all grid
# is filled
def isDraw():
    for i in range(len(labelList)):
        if labelList[i]["ticked"] is False:
            return [False, ""]
    return [True, ""]

# Slave Function for checking board's row for noughts availability, list index
# example:
# [(0,0) -> (0,1) -> (0,2)], 
# [(1,0) -> (1,1) -> (1,2)], 
# [(2,0) -> (2,1) -> (2,2)]
def rowCheck():
    noughtsList = []
    tempLabelList = []
    winner = False
    winnerSign = ""
    for i in range(len(labelList)):
        noughtsList.append(labelList[i]["symbol"])
        tempLabelList.append(labelList[i])
        if (i + 1) % 3 == 0:
            if (noughtsList[0] == noughtsList[1] == noughtsList[2]):
                if noughtsList[0] != "":
                    winner = True
                    winnerSign = noughtsList[0]
            noughtsList = []
            tempLabelList = []
    return [winner, winnerSign]

# Slave Function for checking board's column for noughts availability, list index
# example:
# [(0,0) -> (1,0) -> (2,0)], 
# [(0,1) -> (1,1) -> (2,1)],
# [(0,2) -> (1,2) -> (2,2)]
def colCheck():
    winner = False
    winnerSign = ""
    for i in range(colNumber):
        if labelList[i]["symbol"] == labelList[i+colNumber]["symbol"] == labelList[i+colNumber+colNumber]["symbol"]:
            if labelList[i]["symbol"] != "":
                winner = True
                winnerSign = labelList[i]["symbol"]
    return [winner, winnerSign]

# Slave Function for checking board's diagonal for noughts availability, list 
# index example:
# [(0,0) ->       -> (2,2)], 
# [      -> (1,1) ->      ],
# [(0,0) ->       -> (2,2)]
def diagCheck():
    winner = False
    winnerSign = ""
    i = 0
    j = 2

    # top left to bottom right 
    a = labelList[i]["symbol"]
    b = labelList[i+(colNumber+1)]["symbol"]
    c = labelList[(colNumber+colNumber)+(i+1)]["symbol"]
    d = labelList[j]["symbol"]
    e = labelList[j+(colNumber-1)]["symbol"]
    f = labelList[j+(colNumber+1)]["symbol"]
    if a == b == c:
        print("rt")
        if a != "":
            winner = True
            winnerSign = a

    # bottom left to top right 
    elif d == e == f:
        if d != "":
            winner = True
            winnerSign = d
    else:
        winner = False
    return [winner, winnerSign]

# Render the GUI
window.mainloop()