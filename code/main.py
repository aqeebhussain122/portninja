#!/usr/bin/python
# PORTNINJA: PORT SCANNER DESIGNED TO PERFORM NETWORK RECON OPERATIONS
import sys
import socket
import select
import os
import subprocess

def progCheck():
	if len(sys.argv) < 3 and sys.argv[1] == "" and sys.argv[2] == '':
		print 'Usage: python main.py (IP Address) (port)'
		sys.exit(1)
	else:
		return

# Function which checks for a port state open or closed using the TCP protocol
def TCPportCheck(ip_addr, port_temp):
	try:
        	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if sock == socket.error():
			print "Error creating the socket {}".format(sock)
        	result = sock.connect_ex((ip_addr, port_temp))
		if result == 0:
        	       print("Port {} open".format(port_temp))
       		else:
        	       print("Port {} is closed".format(port_temp))
        	return result
	except:
		return
	finally:
		sock.close()

#def dnsBannerGrab():

	# SOURCE CODE
	# UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# connection = socket

	# PSEUDOCODE
	# Create a socket
	# Embed a subprocess over the wire
	# Error handle to see if the OS is UNIX compliant
	# Error handle if the DNS server is BIND or not
	# Can probably combine above two
	# If OS is UNIX and server is BIND then do the subprocess
	# Using the info from README, this should be able to banner grab a bind server

def protocolCheck(port_num):
	# Added list of protocols based by names and common port numbers
	if(port_num == 22):
		print("Protocol: SSH")
	elif(port_num == 53):
		print("Protocol: DNS")
	elif(port_num == 21):
		print("Protocol: Telnet")
	return port_num

# def sendUDP():
#		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

# def scapyCraftRST():
# Manage all sockets by open and close within functions

def TCPbannerGrab(ip_addr, port_num):
# WORKS WITH TCP CONNECTIONS ONLY
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
		else:
			print('Banner is {}'.format(str(result)))
			return result
	except IOError as error:
		sock.settimeout(5.0)
		if sock == socket.error:
			print("Making the socket didn't work :(")
		print("Exception", error)
	finally:
		sock.close()

def main():
	ip = (str(sys.argv[1]))
	port = int((sys.argv[2]))
	print('IP Address is: ' + ip)
	TCPportCheck(ip, port)
	TCPbannerGrab(ip, port)

if __name__ == '__main__':
	main()

