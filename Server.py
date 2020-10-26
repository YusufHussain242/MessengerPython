import socket
import threading

headerSize = 4
clients = []
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(), 7777))


def handleDisconnect(_clientSocket, _address):
    print(f"{_address} has disconnected")
    clients.remove(_clientSocket)


def sendData(data, _socket):
    dataBytes = bytearray(data, "utf-8")
    dataBytes[0:0] = len(data).to_bytes(headerSize, "little")
    _socket.send(bytes(dataBytes))


def recieveData(_clientSocket, _address):
    print(f"{_address} has connected")
    while True:
        packetSize = 0
        message = ""

        try:
            message = _clientSocket.recv(headerSize)
        except ConnectionResetError:
            handleDisconnect(_clientSocket, _address)
            break

        if len(message) > 0:
            packetSize = int.from_bytes(message, "little")

            message = _clientSocket.recv(packetSize)
            message = message.decode("utf-8")

            print(message)
        else:
            handleDisconnect(_clientSocket, _address)
            break


while True:
    serverSocket.listen(10)
    clientSocket, address = serverSocket.accept()
    thread = threading.Thread(target=recieveData, args=[clientSocket, address])
    thread.start()
    clients.append(clientSocket)

input()
