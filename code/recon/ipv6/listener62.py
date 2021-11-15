#!/usr/bin/python3

import socket
import struct
import sys

interface = sys.argv[1]

# Listening on IPv6 on the local machine
local_addr = '::'
# Multicast address upon which you will be listening. 
mcast_addr = "ff16::fe"
# Port of the MCAST server since ICMPv6 is not being used, we need ports.
mcast_port = 5000
# Name of the interface being used.
ifn = interface

# Create an IPv6 socket of type UDP.
sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Set multicast interface
ifi = socket.if_nametoindex(ifn)
ifis = struct.pack("I", ifi)
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_IF, ifis)

# Set multicast group to join
group = socket.inet_pton(socket.AF_INET6, mcast_addr) + ifis
sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, group)

sock_addr = socket.getaddrinfo(local_addr, mcast_port, socket.AF_INET6, socket.SOCK_DGRAM)[0][4]
sock.bind(sock_addr)

cmd = ""
while True:
    print("Listening on {}:{}".format(mcast_addr, mcast_port))
    data, src = sock.recvfrom(1024)
    print("From " + str(src) + ": " + data.decode())
