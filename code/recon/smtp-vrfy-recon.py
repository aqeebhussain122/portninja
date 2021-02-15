#!/usr/bin/python3
import socket
import sys
import time

target = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to SMTP server")
sock.connect((target, 25))
banner = sock.recv(1024)

print(banner)

with open('test_list.txt') as fp:
	lines = fp.readlines()
	for line in lines:
		sock.send(b'VRFY %b' % line.encode())
		time.sleep(5)
		answerUsername = sock.recv(1024)
		print(answerUsername)
