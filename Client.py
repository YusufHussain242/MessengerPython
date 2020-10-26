import socket

headerSize = 4

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 7777))

while True:
    packetSize = 0
    message = ""

    message = serverSocket.recv(headerSize)
    if len(message) > 0:
        packetSize = int.from_bytes(message, "little")
        print(packetSize)

        message = serverSocket.recv(packetSize)
        message = message.decode("utf-8")

        print(message)
    else:
        break

input()
