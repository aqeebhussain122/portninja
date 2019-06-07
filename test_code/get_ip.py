import socket

# UDP Packet
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Connect to non-existent source
sock.connect(('10.0.0.255', 1))
# Retrieve the IP from the connected socket
IP = sock.getsockname()[0]
print(IP)
