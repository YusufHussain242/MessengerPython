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
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 7777))


def recieveData():
    while True:
        buffer = bytearray()

        try:
            buffer = serverSocket.recv(headerSize+1)
        except ConnectionAbortedError:
            break
        except ConnectionResetError:
            print("Disconnected from server")

        if len(buffer) > 0:
            packetSize = int.from_bytes(buffer, "little")
            varName = buffer[headerSize]

            buffer = serverSocket.recv(packetSize)
            handleData(buffer, varName)
        else:
            break


def handleData(data, varName):
    newData = pickle.loads(data)
    try:
        vars[varName](newData)
    except TypeError:
        vars[varName] = newData

    return newData


def encodeData(data, varName):
    dataBytes = bytearray(pickle.dumps(data))
    dataBytes[0:0] = len(dataBytes).to_bytes(4, "little") + \
        varName.value.to_bytes(1, "little")
    return bytes(dataBytes)


def sendData(data, varName):
    dataBytes = encodeData(data, varName)
    serverSocket.send(dataBytes)


rThread = threading.Thread(target=recieveData)
rThread.start()

while True:
    message = input()
    if message != "":
        sendData([message], V.printMessage)
    else:
        serverSocket.close()
        break

input()
