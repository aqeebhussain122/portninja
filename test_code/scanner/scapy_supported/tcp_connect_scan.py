#!/usr/bin/python3

import socket
import sys
import port_checks
from struct import *

# Global list to store the error messages
error_msg = []

def usage():
        if(len(sys.argv) <= 2):
                print('Not enough arguments')
                return 1

def main():
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        usage()
        dest_ip = (str(sys.argv[1]))
        dest_port = (int(sys.argv[2]))
       # print(('Packet size is {}'.format(result)))

        port_status = port_checks.TCPportCheck(dest_ip, dest_port)
        port_banner = port_checks.TCPbannerGrab(dest_ip, dest_port)
        # TO TEST THIS PROGRAM LAUNCH IN PYTHON AND OPEN WIRESHARK ON THE SPECIFIED NETWORK INTERFACE

main()
