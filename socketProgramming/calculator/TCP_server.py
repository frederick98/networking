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

'serverHost = socket.gethostname()'
serverHost = "localhost"
serverPort = int(input("Masukkan port yang akan digunakan oleh server: "))

operatorList = ['+', '-', '/', '*', '%', 'mod', 'sqr', 'sqrt']

# create socket object
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind socket with the host & port
serverSocket.bind((serverHost, serverPort))

# waiting for client connection
serverSocket.listen(5)
print("Mathematical expression calculator server is ready to use!")

while True:
    # establish connection with client, then send report
    connection, address = serverSocket.accept()
    print('Connection received from ' + str(address))
    while True:
        try:
            expression = connection.recv(1024)
            expression = expression.decode()
            if(expression != 'end'):
                print("Received from client " + str(address) + ": " + str(expression))
                # calculate expression
                result = eval(expression)
                print("passed", result)
                
                # send expression
                print("Sent to client " + str(address) + ": " + str(result))
                connection.send(str(result).encode())
            else:
                connection.send(str("Connection is closing...").encode())
                break
        except(ZeroDivisionError):
            connection.send("Please check expression, you can't divide by 0!".encode())
        except(SyntaxError):
            connection.send("Please check your syntax!".encode())
        except(NameError):
            connection.send("Please insert expression!".encode())

# end connection        
connection.close()

# =============================================================================
# class ClientThread(threading.Thread):
#     def __init__(self,clientAddress,clientsocket):
#         threading.Thread.__init__(self)
#         self.csocket = clientsocket
#         print ("New connection added: ", clientAddress)
#     def run(self):
#         print ("Connection from : ", address)
#         #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
#         msg = ''
#         while True:
#             data = self.csocket.recv(2048)
#             msg = data.decode()
#             if msg=='bye':
#               break
#             print ("from client", msg)
#             self.csocket.send(bytes(msg,'UTF-8'))
#         print ("Client at ", address , " has disconnected...")
# 
# 
# =============================================================================
