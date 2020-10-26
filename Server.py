import socket


def sendData(data, _socket):
    dataBytes = bytes(f"{len(data):<10}" + data, "utf-8")
    print(dataBytes)
    _socket.send(dataBytes)


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(), 7777))
serverSocket.listen(10)

while True:
    clientSocket, address = serverSocket.accept()
    print(f"Connection from {address} has been established!")
    sendData("Welcome to the server!", clientSocket)
    clientSocket.close()

input()
