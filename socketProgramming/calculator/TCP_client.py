# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 22:40:31 2021

@author: frederick_2016730040
"""

"""
library needed
"""
import socket

try:
    # create socket object
    #host = socket.gethostname()
    serverHost = "localhost"
    serverPort = int(input("Masukkan port yang sama dengan server: "))
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # connect to server at port: serverPort
    clientSocket.connect((serverHost, serverPort))
    
    message = 'start'
    while message.lower().strip() != 'end':
        if(message.lower().strip() == ''):
            message ='end'
            clientSocket.send(message.encode("UTF-8"))
        else:
            message = input("Insert mathematical expression: ")
            clientSocket.send(message.encode("UTF-8"))
            
            received = clientSocket.recv(1024).decode()
            print("Results received from server: ", received)
    # close socket when 'end' command received
    clientSocket.close()
    
except(IndexError, ValueError):
    print("Insert correct port number!")