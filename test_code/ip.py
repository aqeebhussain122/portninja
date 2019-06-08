import socket

def get_ip():
	# UDP Packet
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# Connect to non-existent source
		sock.connect(('10.0.0.255', 1))
		# Retrieve the IP from the connected socket
		IP = sock.getsockname()[0]
	except:
		IP = '127.0.0.1'
	finally:
		sock.close()
	return IP

