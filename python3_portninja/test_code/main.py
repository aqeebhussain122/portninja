#!/usr/bin/python
# PORTNINJA: PORT SCANNER DESIGNED TO PERFORM NETWORK RECON OPERATIONS
import sys
import socket
import select
import os
import subprocess
import syn_flood
import ports
import argparse

def main():
	syn_flood.permissions()
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        syn_flood.createSock(s)
	parser = argparse.ArgumentParser(description='SYN Scan and flood tool which forms raw packets taking required IP addresses and port numbers')
        parser.add_argument("sip", help='Source IP Address to form packet', type=str)
        parser.add_argument("dip", help='Destination IP address to form packet', type=str)
	parser.add_argument("sport", help='Source port to form packet', type=int)
	parser.add_argument("dport", help='Destination port to form packet', type=int)
	parser.add_argument("-f", "--flood", help="SYN Flood option to send arbituary number of packets to flood device or network", type=int)
	# Ports switch which takes a list of ports and stores them for processing
	# Elements in ports list to be accessed one by one and given to port check function
	parser.add_argument("-p", "--ports", help="Port switch  which will take a number of ports and scan them against destination ip", type=int, nargs='+')
	parser.add_argument("-s", "--sweep", help="Ping sweep through the network", action='store_true')
        args = parser.parse_args()

        ip_header = syn_flood.ipCreate(args.sip, args.dip)
        tcp_header = syn_flood.tcpCreate(args.sip, args.dip, args.sport, args.dport)
        packet = ip_header + tcp_header
	ports.portNumLimit(args.sport)
	ports.portNumLimit(args.dport)
	print(('IP Address is: ' + args.dip))
	ports.TCPportCheck(args.dip, args.dport)
	print('Performing banner grab')
	ports.TCPbannerGrab(args.dip, args.dport)

	# Checks for additional switches after the primary port check and banner grab
	if args.flood:
		print("Flood option selected: Sending packets...")
		i = 0
		value = int(args.flood)
		while i < value:
			i += 1
			print(("Packets sent: {}".format(i)))
			result = s.sendto(packet, (args.dip, 0))
	if args.ports:
		for port in args.ports:
			check_success = ports.TCPportCheck(args.dip, port)
			check_banner = ports.TCPbannerGrab(args.dip, port)
	if args.sweep:
		for i in range(1, 65565):
			sweep_check = ports.TCPportCheck(args.dip, i)

if __name__ == '__main__':
	main()

# Working version of Python - Python 2.7.15rc1

