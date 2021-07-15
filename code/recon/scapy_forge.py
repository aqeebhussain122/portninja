from scapy.all import *

target_port = 22
tcpRequest = IP(src='192.168.0.16',dst='192.168.0.46')/TCP(sport=5000, dport=22,flags="S")
tcpResponse = sr1(tcpRequest,timeout=1,verbose=0)
try:
	# If a SYN/ACK comes back then the port responded
	if tcpResponse.getlayer(TCP).flags == "SA":
		print("Port {} is listening".format(target_port))

except AttributeError:
	print(target_port,"is not listening")
	print("Scan went through but it didn't go through, I'm sorry")
