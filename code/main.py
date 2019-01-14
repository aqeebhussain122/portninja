#!/usr/bin/python
# PORTNINJA: PORT SCANNER DESIGNED TO PERFORM NETWORK RECON OPERATIONS
import sys
import socket
import select
import os
import subprocess


def progCheck():
	if len(sys.argv) < 3:
		print 'Usage: python main.py (IP Address) (port)'
		sys.exit(1)
	else:
		return

def portNumLimit(port):
	MAX = 65535
	if port < 1 or port > MAX:
		print("Error: Ensure the specified port number is within the limit of: 1 - {}".format(MAX))
		sys.exit(1)
	else:
		return port

# Function which checks for a port state open or closed using the TCP protocol
def TCPportCheck(ip_addr, port_temp):
	try:
		# Socket is created within the function
        	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if sock == socket.error():
			print "Error creating the socket {}".format(sock)
		# Variable assigned to check the connectivity state of a port
        	result = sock.connect_ex((ip_addr, port_temp))
		if result == 0:
        	       print("Port {} open".format(port_temp))
		       sock.close()
       		else:
        	       print("Port {} is closed".format(port_temp))
		sock.close()
        	return result
	except:
		return
	finally:
		# Assurance the socket is closed after use
		sock.close()

# Prototype function (Needs to be improved) - NOT IMPLEMENTED OR TESTED
def protocolCheck(port_num):
	# Added list of protocols based by names and common port numbers
	if(port_num == 22):
		print("Protocol: SSH")
	elif(port_num == 53):
		print("Protocol: DNS")
	elif(port_num == 21):
		print("Protocol: Telnet")
	return port_num

def TCPbannerGrab(ip_addr, port_num):
# WORKS WITH TCP CONNECTIONS ONLY
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	connection = sock.connect_ex((ip_addr, port_num))
	connection = sock.connect_ex((ip_addr, port_num))
	try:
		sock.send(b'GET HTTP/1.1 \r\n')
		sock.settimeout(5.0)
		result = sock.recv(1024)
		# Check for HTTP presence in port number and issue a HTTP HEADER REQUEST
		if port_num == 80:
			sock.send('HEAD / HTTP/1.1\nHost:' + ip_addr + '\n\n')
			print("HTTP header is: ")
		if result == "" or None:
			print("Banner not showing up :(")
			sock.close()
		else:
			print('Banner is {}'.format(str(result)))
			sock.close()
			return result
	except IOError as error:
		sock.settimeout(5.0)
		if sock == socket.error:
			print("Making the socket didn't work :(")
		print("Exception", error)
	finally:
		sock.close()

def main():
	progCheck()
	ip = (str(sys.argv[1]))
	port = int((sys.argv[2]))
	portNumLimit(port)
	print('IP Address is: ' + ip)
	#IPaddressCheck()
	TCPportCheck(ip, port)
	TCPbannerGrab(ip, port)

if __name__ == '__main__':
	main()

# Working version of Python - Python 2.7.15rc1

