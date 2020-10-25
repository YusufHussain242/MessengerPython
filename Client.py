import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 7777))

fullMessage = ""
while True:
    message = serverSocket.recv(8)

    if len(message) <= 0:
        break
    else:
        fullMessage = fullMessage + message.decode("utf-8")

print(fullMessage)
input()
