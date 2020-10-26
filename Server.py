import socket
import threading
import struct
from enum import Enum


class T(Enum):
    null = 0
    string = 1
    int = 2
    float = 3
    function = 4


class V(Enum):
    null = 0
    username = 1
    printMessage = 2


headerSize = 4
clients = []
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(), 7777))


def handleDisconnect(_clientSocket, _address):
    print(f"{_address} has disconnected")
    clients.remove(_clientSocket)


def encodeData(data, dataType, varName):
    dataBytes = bytearray(struct.pack("i", len(data)))

    dataBytes[len(dataBytes):len(dataBytes)] = \
        dataType.value.to_bytes(1, "little")

    dataBytes[len(dataBytes):len(dataBytes)] = \
        varName.value.to_bytes(1, "little")

    def caseString():
        dataBytes[len(dataBytes):len(dataBytes)] = \
            struct.pack(f"{len(data)}s", bytes(data, "utf-8"))

    def caseInt():
        dataBytes[len(dataBytes):len(dataBytes)] = \
            bytearray(struct.pack("i", data))

    def caseFloat():
        dataBytes[len(dataBytes):len(dataBytes)] = \
            (struct.pack("f", data))

    switch = {
        T.string: caseString,
        T.int: caseInt,
        T.float: caseFloat
    }

    switch.get(dataType)()

    return bytes(dataBytes)


def sendData(data, dataType, varName, _sockets):
    dataBytes = encodeData(data, dataType, varName)
    for _socket in _sockets:
        _socket.send(dataBytes)


def broadcastData(data, dataType, varName, exemptions, piggyback):
    if piggyback is False:
        dataBytes = encodeData(data, dataType, varName)
    else:
        dataBytes = data

    culledClients = []
    for c in clients:
        culledClients.append(c)

    for e in exemptions:
        culledClients.remove(e)

    for client in culledClients:
        client.send(dataBytes)


def recieveData(_clientSocket, _address):
    print(f"{_address} has connected")
    while True:
        # packetSize = 0
        buffer = bytearray()
        fullBuffer = bytearray()

        try:
            buffer = _clientSocket.recv(headerSize+2)
            fullBuffer[0:0] = buffer
        except ConnectionResetError:
            handleDisconnect(_clientSocket, _address)
            break

        if len(buffer) > 0:
            packetSize = struct.unpack("i", buffer[:headerSize])[0]
            dataType = buffer[headerSize]
            varType = buffer[headerSize+1]

            buffer = _clientSocket.recv(packetSize)
            fullBuffer[len(fullBuffer):len(fullBuffer)] = buffer

            buffer = struct.unpack(f"{len(buffer)}s", buffer)

            print(dataType, varType, buffer)
            broadcastData(fullBuffer, T.null, V.null, [_clientSocket], True)
        else:
            handleDisconnect(_clientSocket, _address)
            break


def waitForConnect():
    while True:
        serverSocket.listen(10)
        clientSocket, address = serverSocket.accept()
        thread = threading.Thread(target=recieveData,
                                  args=[clientSocket, address])
        thread.start()
        clients.append(clientSocket)


listThread = threading.Thread(target=waitForConnect)
listThread.start()
while True:
    serverMessage = input()
    broadcastData(serverMessage, T.string, V.printMessage, [])
input()
