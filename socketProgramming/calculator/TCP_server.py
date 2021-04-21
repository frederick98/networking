# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 22:48:32 2021
@author: frederick_2016730040
"""

"""
library needed
"""
import socket
import threading
#from sympy import symbols, solve

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        print ("New connection added: ", clientAddress)
    def run(self):
        #print ("Connection received from : ", clientAddress)
        #self.clientSocket.send(bytes("Welcome, parsing connection... done.",'utf-8'))
        
        expression = ''
        while True:
            try:
                expression = self.clientSocket.recv(1024)
                expression = expression.decode()
                if(expression != 'end'):
                    print("Received from client " + str(clientAddress) + ": " + str(expression))
                    # calculate expression
                    result = eval(expression)
                    
                    # buat test hasilnya
                    #print("passed", result)
                    
                    # send expression
                    print("Sent to client " + str(clientAddress) + ": " + str(result))
                    self.clientSocket.send(str(result).encode())
                else:
                    self.clientSocket.send(str("Connection is closing...").encode())
                    self.clientSocket.close()
                    break
            except(ZeroDivisionError):
                self.clientSocket.send("Please check expression, you can't divide by 0!".encode())
            except(SyntaxError):
                self.clientSocket.send("Please check your syntax!".encode())
            except(NameError):
                self.clientSocket.send("Please insert expression!".encode())

        
'serverHost = socket.gethostname()'
serverHost = "localhost"
serverPort = int(input("Write a port number to be used: "))

operatorList = ['+', '-', '/', '*', '%', 'mod', 'sqr', 'sqrt']

# create socket object
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind socket with the host & port
serverSocket.bind((serverHost, serverPort))

print("Mathematical expression calculator server is ready to use!")

while True:
    # waiting for client connection
    serverSocket.listen(1)
    
    # received new connection, start a new thread
    clientSock, clientAddress = serverSocket.accept()
    newThread = ClientThread(clientAddress, clientSock)
    newThread.start()
