import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 7777))

while True:
    packetSize = 0
    message = ""

    message = serverSocket.recv(10)
    if len(message) <= 0:
        packetSize = int(message.decode("utf-8"))

        message = serverSocket.recv(packetSize)
        message = message.decode("utf-8")

        print(message)
    else:
        break

input()
