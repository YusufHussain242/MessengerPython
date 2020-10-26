import socket
import threading
from enum import Enum
import struct


class T(Enum):
    null = 0
    string = 1
    int = 2
    float = 3
    function = 4
    list = 5


class V(Enum):
    null = 0
    username = 1
    printMessage = 2


vars = []
for var in V:
    vars.append(0)

headerSize = 4
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 7777))


def recieveData():
    while True:
        # packetSize = 0
        buffer = bytearray()

        try:
            buffer = serverSocket.recv(headerSize+2)
        except ConnectionAbortedError:
            break

        if len(buffer) > 0:
            packetSize = struct.unpack("i", buffer[:headerSize])[0]
            dataType = buffer[headerSize]
            varName = buffer[headerSize+1]

            buffer = serverSocket.recv(packetSize)
            handleData(buffer, dataType, varName)
            print(vars[varName])
        else:
            break


def handleData(data, dataType, varName):
    newData = ""

    def caseString():
        newData = struct.unpack(f"{len(data)}s", data)[0]
        return newData.decode("utf-8")

    def caseInt():
        return struct.unpack("i", data)[0]

    def caseFloat():
        return struct.unpack("f", data)[0]

    switch = {
        T.string.value: caseString,
        T.int.value: caseInt,
        T.float.value: caseFloat
    }
    newData = switch.get(dataType)()

    vars[varName] = newData

    return newData


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


def sendData(data, dataType, varName):
    dataBytes = encodeData(data, dataType, varName)
    serverSocket.send(dataBytes)


rThread = threading.Thread(target=recieveData)
rThread.start()

while True:
    message = input()
    if message != "":
        sendData(message, T.string, V.printMessage)
    else:
        serverSocket.close()
        break

input()
