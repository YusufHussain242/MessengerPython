import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 7777))

message = recv(1024)
print(message.decode("utf-8"))

input()
