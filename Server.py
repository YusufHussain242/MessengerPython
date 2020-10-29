import socket
import threading
import pickle
from enum import Enum


class V(Enum):
    null = 0
    username = 1
    printMessage = 2


vars = []
for var in V:
    vars.append(0)


# args = [message]
def _printMessage(args):
    print(args[0])


vars[V.printMessage.value] = _printMessage

headerSize = 4
clients = []
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(), 7777))


def handleDisconnect(_clientSocket, _address):
    print(f"{_address} has disconnected")
    clients.remove(_clientSocket)


def encodeData(data, varName):
    dataBytes = bytearray(pickle.dumps(data))
    dataBytes[0:0] = len(dataBytes).to_bytes(4, "little") + \
        varName.value.to_bytes(1, "little")
    return bytes(dataBytes)


def handleData(data, varName):
    newData = pickle.loads(data)
    try:
        vars[varName](newData)
    except TypeError:
        vars[varName] = newData

    return newData


def sendData(data, varName, _sockets):
    dataBytes = encodeData(data, varName)
    for _socket in _sockets:
        _socket.send(dataBytes)


def broadcastData(data, varName, exemptions=[], piggyback=False):
    if piggyback is False:
        dataBytes = encodeData(data, varName)
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
        buffer = bytearray()
        fullBuffer = bytearray()

        try:
            buffer = _clientSocket.recv(headerSize+1)
            fullBuffer = buffer
        except ConnectionResetError:
            handleDisconnect(_clientSocket, _address)
            break

        if len(buffer) > 0:
            packetSize = int.from_bytes(buffer[:headerSize], "little")
            varName = buffer[headerSize]

            buffer = _clientSocket.recv(packetSize)
            fullBuffer = fullBuffer + buffer
            handleData(buffer, varName)

            broadcastData(fullBuffer, V.null, [_clientSocket], True)
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
    broadcastData([serverMessage], V.printMessage)
input()
