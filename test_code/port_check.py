#!/usr/bin/python3
import socket
import sys

def main():
    port = int(sys.argv[1])
    if port <= 0 or port >= 65535:
        print("Error: Port number is too high/low")

def portNumLimit(port):
    MAX = 65535
    if port < 1 or port > MAX:
        print(("Error: Ensure the specified port number is within the limit of: 1 - {}".format(MAX)))
        sys.exit(1)
    else:
	return port


main()
