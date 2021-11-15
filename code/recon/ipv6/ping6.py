import time
import random
import struct
import select
import socket
import sys

#https://docs.python.org/3/library/struct.html
# s = string
# b = integer value
# https://stackoverflow.com/questions/20905770/checksum-icmp-python-with-wireshark#20905906
"""
def chk(data):
    x = sum(x << 8 if i % 2 else x for i, x in enumerate(data)) & 0xFFFFFFFF
    x = (x >> 16) + (x & 0xFFFF)
    x = (x >> 16) + (x & 0xFFFF)
    return struct.pack('<H', ~x & 0xFFFF)

# Send a ping message. Studying this code. Stick some data into an ICMP packet and then exfiltrate it.
def ping(addr, timeout=1, number=1, data=b''):
    # Using a Datagram socket, send a ping message. 
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP) as conn:
        # Network byte order.
        payload = struct.pack('!HH', random.randrange(0, 65536), number) + data

        conn.connect((addr, 80))
        conn.sendall(b'\x08\0' + chk(b'\x08\0\0\0' + payload) + payload)
        start = time.time()

        while select.select([conn], [], [], max(0, start + timeout - time.time()))[0]:
            data = conn.recv(65536)
            if len(data) < 20 or len(data) < struct.unpack_from('!xxH', data)[0]:
                continue
            if data[20:] == b'\0\0' + chk(b'\0\0\0\0' + payload) + payload:
                return time.time() - start


if __name__ == '__main__':
    print(ping('192.168.0.56'))
"""

# https://stackoverflow.com/questions/65285314/python3-socket-sending-multicast-message-over-ipv6-uses-different-interface-eve


interface = sys.argv[1]

# Get the interface number of the target interface on the internal network
interface_number = socket.if_nametoindex(interface)
print(interface_number)
# Iniialise a UDP socket which will be of type IPv6
udp_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# Reuse the address/
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Let our messages come back to us.
udp_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
udp_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 255)
addrinfo = socket.getaddrinfo("ff02::1", None)[0]  # multicast group is ff02::1
group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
mreq = group_bin + struct.pack("@I", int(interface_number))  # socket.if_nametoindex("eth0")  gives 2
udp_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
udp_socket.setsockopt(socket.IPPROTO_IPV6,socket.IPV6_MULTICAST_IF,0)
#udp_socket.bind(('::1', 8080))
bind = udp_socket.bind(('::1', 8080))
send = udp_socket.sendto(bytes([1, 2, 3, 4]), ("ff02::1", 13500))

print(udp_socket)
print(addrinfo)
print(mreq)
print(send)
print(bind)

