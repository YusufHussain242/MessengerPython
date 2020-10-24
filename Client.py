import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 7777))

while True:
  fullMessage = ""
  
  while True:
    message = serverSocket.recv(8)
    if len(message) == 0:
      break;
    fullMessage.append(message)

  print(fullMessage.decode("utf-8"))

input()