#!/usr/bin/python3

import socket
import sys

target = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((target, 25))
banner = sock.recv(1024)

print(banner)
sock.send(b'VRFY root \r\n')
answerUsername = sock.recv(1024)

print(answerUsername)
