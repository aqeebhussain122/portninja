import time
import random
import struct
import select
import socket

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
#https://github.com/krabelize/icmpdoor/blob/main/icmpdoor.py

# Use subprocess to translate the commands to utf-8 and then execute them via each side. 
# Payload data which eventually needs to lead to reverse shell
ICMP_CODE = 41
payload_data = b'somedata'
payload = struct.pack('!HH', random.randrange(0,65536), int(ICMP_CODE)) + payload_data
print(payload)

# Create a non-root datagram
icmp_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_ICMPV6)
#icmp_sock = socket.socket(socket.SOCK_DGRAM, socket.IPPROTO_ICMPV6)
# Connect to the target on port 0. Doesn't matter because iCMP does not work on port level
icmp_sock.connect(('::1', 0))
# Send all pf the data as an ICMP echo request message code number 128 for ICMPv6
send = icmp_sock.sendall(b'\x80\0' + payload)
print(send)

# Cpnverting the given values into bytes

#RFC1700 stated it must be so. (and defined network byte order as big-endian).

ICMP_ECHO_REQUEST = 128
# Protocol number


# Generate the payload to pack the data up to send through the wire.

#icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
#print(icmp_sock.connect(('192.168.0.56', 22)))
