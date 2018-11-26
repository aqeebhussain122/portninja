#!/usr/bin/python

import socket
import sys
from scapy.all import *
from struct import *

# Global list to store the error messages
msg = []

def main():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error, msg:
		# Include in portninja
		print socket.error + 'Socket could not be created. Error code: ' + str(msg[0]) + ' Message ' + msg[1]

# Checksum which will be passed to verify
def checksum(msg):
	s = 0
	for i in range(0, len(msg), 2):
		w = (ord(msg[i]) << 8) + (ord(msg[i+1]))
		s += w

	s = (s >> 16) + (s & 0xffff)
	s = ~s & 0xffff

	return s


# Raw socket creation
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#	s = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
except socket.error, msg:
	print 'Socket could not be created. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

# Kernel will not add headers because we're adding them in
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
#s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
packet = ''

source_ip = '127.0.0.1'
dest_ip = '127.0.0.1'

	# IP header fields
ihl = 5
version = 4
tos = 0
tot_len = 20 + 20
id = 54321
frag_off = 0
ttl = 255
protocol = socket.IPPROTO_TCP
#protocol = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
check = 10 # Checksum succession
saddr = socket.inet_aton(source_ip)
daddr = socket.inet_aton(dest_ip)


ihl_version = (version << 4) + ihl

ip_header = pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)

source = 0
dest = 0
seq = 0
ack_seq = 0
doff = 5

#tcp flags
fin = 0
syn = 1
rst = 0
psh = 0
ack = 0
urg = 0
window = socket.htons(5480)
check = 0
urg_ptr = 0

offset_res = (doff << 4) + 0
tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)

tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags, window, check, urg_ptr)

#pseudo header fields
source_address = socket.inet_aton(source_ip)
dest_address = socket.inet_aton(dest_ip)
placeholder = 0
protocol = socket.IPPROTO_TCP
tcp_length = len(tcp_header)

psh = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
psh += tcp_header

tcp_checksum = checksum(psh)

tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags, window, tcp_checksum, urg_ptr)

packet = ip_header + tcp_header

s.sendto(packet, (dest_ip, 0))


main()
