#!/usr/bin/python

import socket
import sys
from scapy.all import *
from struct import *

# Global list to store the error messages
error_msg = []

# template socket which will be passed to functions
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

# DOCSTRING: SOCKET CREATION using try and catch error handling
def createSock(s):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error as error_msg:
		print 'Socket could not be created. Error code: ' + str(error_msg[0]) + ' Message ' + str(error_msg[1])
	return s

# Calling of the function to create a socket
createSock(s)

# Checksum which will be passed to verify - Contained in function with storage and access to a global list
def checksum(msg):
	s = 0
	for i in range(0, len(msg), 2):
		w = (ord(msg[i]) << 8) + (ord(msg[i+1]))
		s += w
	s = (s >> 16) + (s & 0xffff)
	s = ~s & 0xffff

	return s

createSock(s)

# Kernel will not add headers because we're adding them in

def ipCreate(source_ip, dest_ip):
	s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
	packet = ''

	# IP header fields
	ihl = 5
	version = 4
	tos = 0
	tot_len = 20 + 20
	id = 54321
	frag_off = 0
	ttl = 255
	# Variable giving the socket a protocol of TCP
	protocol = socket.IPPROTO_TCP
	check = 10 # Checksum succession
	saddr = socket.inet_aton(source_ip)
	daddr = socket.inet_aton(dest_ip)

	ihl_version = (version << 4) + ihl

	# IP Header packed up 
	ip_header = pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)
	return ip_header

# Once the header is packed and the function returns it. ip header is created
ip_header = ipCreate('127.0.0.1', '127.0.0.1')

def tcpCreate(source_port, dest_port):
	source_ip = '127.0.0.1'
	dest_ip = '127.0.0.1'
	# source port
	#source_port = 5456
	# destination port
	#dest_port = 80
	seq = 0
	ack_seq = 0
	doff = 5
	#tcp flags
	fin = 0
	# Activation of syn packet to enable syn scan
	syn = 1
	# Reset flag
	rst = 0
	# Push flag
	psh = 0
	# ACKnowledgement flag
	ack = 0
	# Urgent flag
	urg = 0
	# Window size of the scan
	window = socket.htons(5480)
	check = 0
	# Urgent pointer
	urg_ptr = 0

	offset_res = (doff << 4) + 0
	tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)

	# TCP Header packed
	tcp_header = pack('!HHLLBBHHH', source_port, dest_port, seq, ack_seq, offset_res, tcp_flags, window, check, urg_ptr)

	#pseudo header fields
	source_address = socket.inet_aton(source_ip)
	dest_address = socket.inet_aton(dest_ip)
	placeholder = 0
	#TCP Header assigned with TCP protocol
	protocol = socket.IPPROTO_TCP
	tcp_length = len(tcp_header)

	psh = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
	psh += tcp_header

	# Checksum function using push flag
	tcp_checksum = checksum(psh)

	tcp_header = pack('!HHLLBBHHH', source_port, dest_port, seq, ack_seq, offset_res, tcp_flags, window, tcp_checksum, urg_ptr)

	return tcp_header

tcp_header = tcpCreate(5543, 80)

packet = ip_header + tcp_header
# Attempt to check if data has actually been sent
result = s.sendto(packet, ('127.0.0.1', 0))

# TO TEST THIS PROGRAM LAUNCH IN PYTHON AND OPEN WIRESHARK ON THE SPECIFIED NETWORK INTERFACE
