import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect((socket.gethostname(), 7777))

while True:
    message = serverSocket.recv(8)
    print(message.decode("utf-8"))

print("Changes on atom")
print("Even more changes on atom")

input()
