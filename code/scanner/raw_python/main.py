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
        parser.add_argument("-f", "--flood", help="SYN Flood option to send arbituary number of packets to flood device or network", type=int)
        parser.add_argument("-x", "--forge", help="Forge source IP address fields in packets to mask location", type=str)
        # Ports switch which takes a list of ports and stores them for processing
       
        # Ports are currently not in list form which means the first port is scanned first
        parser.add_argument("-p", "--ports", help="Port switch  which will take a number of ports and scan them against destination ip", type=int, nargs='+')
        # Verbose level 1 (Regular scan of top 1,000 ports)
        parser.add_argument("-v1", "--verbose-one", help=" Verbose level 1", type=int)
        parser.add_argument("-s", "--sweep", help="Port sweep through the network", action='store_true')
        args = parser.parse_args()
        ports.portNumLimit(args.source_port)
        ports.portNumLimit(args.destination_port)
        # TCP packets are crafted from scratch - no forgery done unless specified with -s switch
        ip_header = craft.ipCreate('127.0.0.1', args.destination_ip)
        tcp_header = craft.tcpCreate('127.0.0.1', args.destination_ip, args.source_port, args.destination_port)
        packet = ip_header + tcp_header
        #ports.portNumLimit(args.source_port)
        #ports.portNumLimit(args.destination_port)
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
            # List comprehension prevents the first port from being scanned again
            for port in args.ports[0:]:
                        check_success = ports.TCPportCheck(args.destination_ip, port)
                        check_banner = ports.TCPbannerGrab(args.destination_ip, port)

        # Sweep all ports on a machine - freezing up on the first attempt 
        if args.sweep:
                for port in range(1, 65565):
                        sweep_check = ports.TCPportCheck(args.destination_ip, port)
                        check_banner = ports.TCPbannerGrab(args.destination_ip, port)
                        time.sleep(2)

        #if args.verbose-one:
        #    print("jshj")


        if args.forge:
           print("Forged IP address: %s" % (args.forge))
           ip_header = craft.ipCreate(args.forge, args.destination_ip)
           tcp_header = craft.tcpCreate(args.forge, args.destination_ip, args.source_port, args.destination_port)
           packet = ip_header + tcp_header
           result = s.sendto(packet, (args.destination_ip, 0))
           #check_success = ports.TCPportCheck(args.destination_ip, args.destination_port)
           #check_banner = ports.TCPbannerGrab(args.destination_ip, args.destination_port)

        print("Flood option was not chosen, sending 1 packet to initiate SYN scan")
        #result = s.sendto(packet, (args.destination_ip, 0))
        #port_status = ports.TCPportCheck(args.destination_ip, args.destination_port)
        #port_banner = ports.TCPbannerGrab(args.destination_ip, args.destination_port)

if __name__ == '__main__':
        main()
