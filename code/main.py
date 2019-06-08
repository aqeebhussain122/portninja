#!/usr/bin/python3
# PORTNINJA: PORT SCANNER DESIGNED TO PERFORM NETWORK RECON OPERATIONS
# Get the primary IP address with a gateway
import ip
import sys
import socket
import select
import os
import subprocess
import ports
import argparse
import craft

def main():
	# Raw socket for raw packet
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	ip_details = ip.get_ip()

	parser = argparse.ArgumentParser(description='SYN Scan and flood tool which forms raw packets taking required IP addresses and port numbers')
	parser.add_argument("destination_ip", help='Destination IP address to form packet', type=str)
	parser.add_argument("source_port", help='Source port to form packet', type=int)
	parser.add_argument("destination_port", help='Destination port to form packet', type=int)
	parser.add_argument("-f", "--flood", help="SYN Flood option to send arbituary number of packets to flood device or network", type=int)
        # Ports switch which takes a list of ports and stores them for processing
        # Elements in ports list to be accessed one by one and given to port check function
	parser.add_argument("-p", "--ports", help="Port switch  which will take a number of ports and scan them against destination ip", type=int, nargs='+')
	parser.add_argument("-s", "--sweep", help="Ping sweep through the network", action='store_true')
	args = parser.parse_args()
	ports.portNumLimit(args.source_port)
	ports.portNumLimit(args.destination_port)
	ip_header = craft.ipCreate(ip_details, args.destination_ip)
	tcp_header = craft.tcpCreate(ip_details, args.destination_ip, args.source_port, args.destination_port)
	packet = ip_header + tcp_header
	ports.portNumLimit(args.source_port)
	ports.portNumLimit(args.destination_port)
	print(('IP Address is: ' + args.destination_ip))
	ports.TCPportCheck(args.destination_ip, args.destination_port)
	print('Performing banner grab')
	ports.TCPbannerGrab(args.destination_ip, args.destination_port)

        # Checks for additional switches after the primary port check and banner grab
	if args.flood:
		print("Flood option selected: Sending packets...")
		i = 0
		value = int(args.flood)
		while i < value:
			i += 1
			print(("Packets sent: {}".format(i)))
			result = s.sendto(packet, (args.destination_ip, 0))
	if args.ports:
		for port in args.ports:
			check_success = ports.TCPportCheck(args.destination_ip, port)
			check_banner = ports.TCPbannerGrab(args.destination_ip, port)

        # Ping sweep all ports on a machine - freezing up on the first attempt 
	if args.sweep:
		for i in range(1, 65565):
			sweep_check = ports.TCPportCheck(args.destination_ip, i)

if __name__ == '__main__':
        main()
