import socket


def sendData(data, _socket):
    dataBytes = bytearray(data, "utf-8")
    dataBytes[0:0] = len(data).to_bytes(headerSize, "little")
    _socket.send(bytes(dataBytes))


headerSize = 4

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(), 7777))
serverSocket.listen(10)

while True:
    clientSocket, address = serverSocket.accept()
    print(f"Connection from {address} has been established!")
    sendData("Welcome to the server!", clientSocket)
    clientSocket.close()

input()
