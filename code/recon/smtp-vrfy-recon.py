#!/usr/bin/python3

import socket
import sys

target = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((target, 25))
banner = sock.recv(1024)
print(banner.decode("utf-8"))

# Sending the VRFY call and seeing if it exists. Every box has root so a good rule of thumb to test
sock.send(b'VRFY root \r\n')

answerUsername = sock.recv(1024)
print(answerUsername.decode("utf-8"))
answerUsername_decoded = answerUsername.decode("utf-8")

answerAsArray = answerUsername_decoded.split(" ")

if answerAsArray[0] == "252":
	print("VRFY works")
else:
	print("VRFY is not present")
