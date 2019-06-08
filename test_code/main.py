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
# Needs to be reorganised and renamed
# import syn_flood -> craft
import craft

def main():
	# Raw socket for raw packet
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        ip_details = ip.get_ip()
			
	# Removed source port from main parser	
        parser = argparse.ArgumentParser(description='SYN Scan and flood tool which forms raw packets taking required IP addresses and port numbers')
        parser.add_argument("dip", help='Destination IP address to form packet', type=str)
        parser.add_argument("sport", help='Source port to form packet', type=int)
        parser.add_argument("dport", help='Destination port to form packet', type=int)
        parser.add_argument("-f", "--flood", help="SYN Flood option to send arbituary number of packets to flood device or network", type=int)
        # Ports switch which takes a list of ports and stores them for processing
        # Elements in ports list to be accessed one by one and given to port check function
        parser.add_argument("-p", "--ports", help="Port switch  which will take a number of ports and scan them against destination ip", type=int, nargs='+')
        parser.add_argument("-s", "--sweep", help="Ping sweep through the network", action='store_true')
        args = parser.parse_args()
        #ports.portNumLimit(ip_details)
        #ports.portNumLimit(args.dip)
        ip_header = craft.ipCreate(ip_details, args.dip)
        tcp_header = craft.tcpCreate(ip_details, args.dip, args.sport, args.dport)
        packet = ip_header + tcp_header
        #ports.portNumLimit(args.sport)
        #ports.portNumLimit(args.dport)
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

        # Ping sweep all ports on a machine - freezing up on the first attempt 
        if args.sweep:
                for i in range(1, 65565):
                        sweep_check = ports.TCPportCheck(args.dip, i)

if __name__ == '__main__':
        main()

# Working version of Python - Python 2.7.15rc1

