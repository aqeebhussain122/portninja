#!/usr/bin/python3
# PORTNINJA: PORT SCANNER DESIGNED TO PERFORM NETWORK RECON OPERATIONS
# Get the primary IP address with a gateway
import sys
import socket
import select
import os
import subprocess
import ports
import argparse
import craft
import time 

def main():
        # Raw socket for raw packet
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        parser = argparse.ArgumentParser(description='SYN Scan and flood tool which forms raw packets taking required IP addresses and port numbers')
        parser.add_argument("destination_ip", help='Destination IP address to form packet', type=str)
        parser.add_argument("source_port", help='Source port to form packet', type=int)
        parser.add_argument("destination_port", help='Destination port to form packet', type=int)

        ports.portNumLimit(args.source_port)
        ports.portNumLimit(args.destination_port)
        ip_header = craft.ipCreate('127.0.0.1', args.destination_ip)
        tcp_header = craft.tcpCreate('127.0.0.1', args.destination_ip, args.source_port, args.destination_port)
        packet = ip_header + tcp_header
        #ports.portNumLimit(args.source_port)
        #ports.portNumLimit(args.destination_port)
        print(('IP Address is: ' + args.destination_ip))

        ports.TCPportCheck(args.destination_ip, args.destination_port)
        print('Performing banner grab')
        ports.TCPbannerGrab(args.destination_ip, args.destination_port)

if __name__ == '__main__':
        main()
