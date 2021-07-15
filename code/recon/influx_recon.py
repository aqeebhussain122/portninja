#!/usr/bin/python3
# PORTNINJA: PORT SCANNER DESIGNED TO PERFORM NETWORK RECON OPERATIONS
# Get the primary IP address with a gateway
import sys
import socket
import select
import os
import subprocess
import argparse
import time 
from struct import *
import argparse

def portNumLimit(port):
    num = int(port)
    MAX = 65535
    if num < 1 or num > MAX:
        print(("Error: Ensure the specified port number is within the limit of: 1 - {}".format(MAX)))
        sys.exit(1)
    else:
        return port

# Function which checks for a port state open or closed using the TCP protocol
def TCPportCheck(ip_addr, port_temp):
    try:
        # Socket is created within the function
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock == socket.error():
            print("Error creating the socket {}".format(sock))
        # Variable assigned to check the connectivity state of a port
        result = sock.connect_ex((ip_addr, port_temp))
        if result == 0:
                   print(("Port {} open".format(port_temp)))
                   sock.close()
        else:
                   print(("Port {} closed".format(port_temp)))
        sock.close()
        return result
    except:
        return
    finally:
        # Assurance the socket is closed after use
        sock.close()

def TCPbannerGrab(ip_addr, port_num):
# WORKS WITH TCP CONNECTIONS ONLY
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # encoding of ip_addr to send a proper HTTP request
    # Primary connection is made through this line - TCP connection
    connection = sock.connect_ex((ip_addr, port_num))
    try:
        sock.send(b'GET HTTP/1.1 \r\n\r\n')
        sock.settimeout(5)
        result = sock.recv(1024)
        # Check for HTTP presence in port number and issue a HTTP HEADER REQUEST
        #if port_num == 80:
            #sock.send(b'HEAD / HTTP/1.1\nHost:' + b'\n' + '\n\n')
        # If the banner contains an empty string but the connection went through

        if result == "" or None:
            print("Banner not showing up :(")
            sock.close()
        else:
            print(('Banner is {}'.format(str(result))))
            sock.close()
            return result
    except IOError as error:
        # Setting 5 seconds to timeout the socket connection when there's an error
        sock.settimeout(5.0)
        if sock == socket.error:
            print("Making the socket didn't work :(")
        print(("Exception", error))
    finally:
        sock.close()

# Add a list or something of all the different ports or something
#def ports_classification():
# Global list to store the error messages
error_msg = []

def createSock(s):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except socket.error as error_msg:
        print('Socket could not be created. Error code: ' + str(error_msg[0]) + ' Message ' + str(error_msg[1]))
    return s

# Calling of the function to create a socket
# Checksum which will be passed to verify - Contained in function with storage and access to a global list

# This function requires further research and correcting
def checksum(msg):
    s = 0
    len_msg = len(msg)
    # Loop to create range from 0 to length of the packet
    for i in range(0, len_msg, 2):
        w = (len_msg << 8) + (len_msg + 1)
        s += w
    s = (s >> 16) + (s & 0xffff)
    s = ~s & 0xffff
    return s

# IPV4 Packet creation 
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

# TCP SYN Packet created using the function which is then fed to pack function, to pack in network bits
def tcpCreate(source_ip ,dest_ip, source_port, dest_port):
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


def port_scan(target):
        #target = sys.argv[1]
        influx_port = 8086
        # Raw socket for raw packet
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        portNumLimit(23812)
        portNumLimit(influx_port)
        ip_header = ipCreate('127.0.0.1', target)
        tcp_header = tcpCreate('127.0.0.1', target, 23812, influx_port)
        packet = ip_header + tcp_header
        print(('IP Address is: ' + target))
        TCPportCheck(target, influx_port)
        print('Performing banner grab')
        TCPbannerGrab(target, influx_port)

def main():
    target = sys.argv[1]
    port_scan(target)

if __name__ == '__main__':
        main()
