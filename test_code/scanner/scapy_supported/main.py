#!/usr/bin/python3
# PORTNINJA: PORT SCANNER DESIGNED TO PERFORM NETWORK RECON OPERATIONS
# Get the primary IP address with a gateway
import sys
import socket
import select
import os
import subprocess
import port_checks
import host_checks
import argparse
import time 
import tcp_syn
import tcp_ack

def main():
        # Raw socket for raw packet
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        parser = argparse.ArgumentParser(description='SYN Scan and flood tool which forms raw packets taking required IP addresses and port numbers')
        parser.add_argument("destination_ip", help='Destination IP address to form packet', type=str)
        parser.add_argument("source_port", help='Source port to form packet', type=int)
        parser.add_argument("destination_port", help='Destination port to form packet', type=int)
        parser.add_argument("-f", "--flood", help="SYN Flood option to send arbituary number of packets to flood device or network", type=int)
        parser.add_argument("-x", "--forge", help="Forge source IP address fields in packets to mask location", type=str)
        # Ports switch which takes a list of port_checks and stores them for processing
       
        # Ports are currently not in list form which means the first port is scanned first
        parser.add_argument("-p", "--port_checks", help="Port switch  which will take a number of ports and scan them against destination ip", type=int, nargs='+')
        # Verbose level 1 (Regular scan of top 1,000 port_checks)
        parser.add_argument("-s", "--syn", help="Sending SYN packets to each target port and then looking for the response being open/closed/filtered", action='store_true')
        parser.add_argument("-w", "--sweep", help="Port sweep through the machine", action='store_true')
        parser.add_argument("-a", "--ack", help="ACK scan a given port to see if filtered or not by stateful firewall", action='store_true')
        args = parser.parse_args()
        port_checks.portNumLimit(args.source_port)
        port_checks.portNumLimit(args.destination_port)
        

        # This section will be developed to work with scapy with various scans which will have their own error handling
        #ip_header = craft.ipCreate('127.0.0.1', args.destination_ip)
        #tcp_header = craft.tcpCreate('127.0.0.1', args.destination_ip, args.source_port, args.destination_port)
        #packet = ip_header + tcp_header
        print('IP Address is: ' + args.destination_ip)
        print("Checking host availability with a ping")
        target_ip_check = host_checks.icmp_check(args.destination_ip)

        port_checks.TCPportCheck(args.destination_ip, args.destination_port)
        print('\n\nPerforming banner grab')
        port_checks.TCPbannerGrab(args.destination_ip, args.destination_port)

        # Checks for additional switches after the primary port check and banner grab
        if args.flood:
                print("Flood option selected: Performing SYN Flood...")
                i = 0
                value = int(args.flood)
                while i < value:
                        i += 1
                        print(("Packets sent: {}".format(i)))
                        result = tcp_syn.send_syn(args.destination_ip, args.destination_port)
                        #result = s.sendto(packet, (args.destination_ip, 0))
        if args.port_checks:
            # List comprehension prevents the first port from being scanned again
            for port in args.port_checks[0:]:
                        check_port_success = port_checks.TCPportCheck(args.destination_ip, port)
                        check_banner = port_checks.TCPbannerGrab(args.destination_ip, port)

        # Sweep all port_checks on a machine - freezing up on the first attempt 
        if args.sweep:
                for port in range(1, 65565):
                        sweep_check = port_checks.TCPportCheck(args.destination_ip, port)
                        check_banner = port_checks.TCPbannerGrab(args.destination_ip, port)
                        time.sleep(2)

        if args.syn:
            for port in args.port_checks[0:]:
                tcp_syn.send_syn(args.destination_ip, port)

        if args.ack:
            for port in args.port_checks[0:]:
                tcp_ack.send_ack(args.destination_ip, port)

        if args.forge:
           print("Forged IP address: %s" % (args.forge))

           '''
           This section is commented 

           ip_header = craft.ipCreate(args.forge, args.destination_ip)
           tcp_header = craft.tcpCreate(args.forge, args.destination_ip, args.source_port, args.destination_port)
           packet = ip_header + tcp_header
           result = s.sendto(packet, (args.destination_ip, 0))
           '''

if __name__ == '__main__':
        main()
