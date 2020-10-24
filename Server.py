import socket

serverSocket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(), 7777))
serverSocket.listen(10)

while True:
  clientSocket , address = serverSocket.accept()
  print(f"Connection from {address} has been established!")
  clientSocket.send(bytes("Welcome to the server!" , "utf-8"))