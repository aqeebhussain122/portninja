import socket

hostname = socket.gethostname()
ip_addr = socket.gethostbyname(hostname)
print("{} {}".format(hostname, ip_addr))
