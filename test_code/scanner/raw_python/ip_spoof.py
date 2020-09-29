#!/usr/bin/python3

import socket
import sys
import ports
from struct import *
import argparse
import time

# Global list to store the error messages
error_msg = []


def createSock():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error as error_msg:
		print('Socket could not be created. Error code: ' + str(error_msg[0]) + ' Message ' + str(error_msg[1]))
	return s

# Calling of the function to create a socket
# Checksum which will be passed to verify - Contained in function with storage and access to a global list
def checksum(msg):
	s = 0
	for i in range(0, len(msg), 2):
		# w = (ord(msg[i]) << 8) + (ord(msg[i+1]))
    # Ord call is removed for code to function correctly with Python
                w = (msg[i]) << 8 + (msg[i+1])
                s += w
	s = (s >> 16) + (s & 0xffff)
	s = ~s & 0xffff
	return s

# IP address is given in as function parameter/argument
def ipCreate(source_ip, dest_ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
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
#ip_header = ipCreate('127.0.0.1', '127.0.0.1')

# SYN Packet is created from the function containing the flags
def tcpCreate(source_ip ,dest_ip, source_port, dest_port):
# IP Values are defined in the function, allowing them to be used more flexibly
#	source_ip = '10.0.2.7'
#	dest_ip = '10.0.2.12'
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

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("source_ip", help="Name of IP address to originate the request from (The spoofed address) ")
        parser.add_argument("source_port", help="Custom port to generate with the spoofed packet", type=int)
        parser.add_argument("destination_ip", help="Name of target IP address to enumerate")
        parser.add_argument("destination_port", help="Target port to enumerate", type=int)
        parser.add_argument("-p", "--ports", help="Port switch  which will take a number of ports and scan them against destination ip", type=int, nargs='+')
        parser.add_argument("sleep_time", help="Quantity of time to sleep before pinging the next host", type=int)
        args = parser.parse_args()

        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

        # ip_header = ipCreate(source_ip, dest_ip)
        ip_header = ipCreate(args.source_ip, args.destination_ip)
        # tcp_header = tcpCreate(source_ip, dest_ip, source_port, dest_port)
        ports.portNumLimit(args.source_port)
        ports.portNumLimit(args.destination_port)
        tcp_header = tcpCreate(args.source_ip, args.destination_ip, args.source_port, args.destination_port)
        packet = ip_header + tcp_header
	# Attempt to check if data has actually been sent - s.sendto(packet, ('source_ip' << THIS DETERMINES SUCCESS), 0 ))
        sleep = time.sleep(args.sleep_time)
        result = s.sendto(packet, (args.destination_ip, 0))
        print(('Packet size is {}'.format(result)))
        print ('Target IP address: {}'.format(args.destination_ip))
        port_status = ports.TCPportCheck(args.destination_ip, args.destination_port)
        print ('Performing banner grab')
        port_banner = ports.TCPbannerGrab(args.destination_ip, args.destination_port)
        #print("{} \n {}".format(port_status, port_banner))
        #print("Port banner is {}".format(port_banner))
	# TO TEST THIS PROGRAM LAUNCH IN PYTHON AND OPEN WIRESHARK ON THE SPECIFIED NETWORK INTERFACE
        if args.ports:
            for port in args.ports:
                ip_header = ipCreate(args.source_ip, args.destination_ip)
                tcp_header = tcpCreate(args.source_ip, args.destination_ip, args.source_port, port)
                ports.portNumLimit(args.source_port)
                ports.portNumLimit(args.destination_port)                
                packet = ip_header + tcp_header
                sleep = time.sleep(args.sleep_time)                
                #result = s.sendto(packet, (args.destination_ip, 0))
                check_success = ports.TCPportCheck(args.destination_ip, port)
                check_banner = ports.TCPbannerGrab(args.destination_ip, port)
main()
