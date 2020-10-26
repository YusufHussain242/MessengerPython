import socket
import threading

headerSize = 4
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 7777))


def recieveData():
    while True:
        packetSize = 0
        message = ""

        try:
            message = serverSocket.recv(headerSize)
        except ConnectionAbortedError:
            break

        if len(message) > 0:
            packetSize = int.from_bytes(message, "little")

            message = serverSocket.recv(packetSize)
            message = message.decode("utf-8")

            print(message)
        else:
            break


def sendData(data):
    dataBytes = bytearray(data, "utf-8")
    dataBytes[0:0] = len(data).to_bytes(headerSize, "little")
    serverSocket.send(bytes(dataBytes))


rThread = threading.Thread(target=recieveData)
rThread.start()

while True:
    message = input()
    if message != "":
        sendData(message)
    else:
        serverSocket.close()
        break

input()
