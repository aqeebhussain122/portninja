#!/usr/bin/python3
import socket

import sys

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
                   print(("Port {} is closed".format(port_temp)))
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

    # Primary connection is made through this line - TCP connection
    connection = sock.connect_ex((ip_addr, port_num))
    try:
        sock.send(b'GET HTTP/1.1 \r\n\r\n')
        sock.settimeout(5)
        result = sock.recv(1024)
        # Check for HTTP presence in port number and issue a HTTP HEADER REQUEST
        if port_num == 80:
            #sock.send('HEAD / HTTP/1.1\nHost:' + ip_addr + '\n\n')
            print("HTTP header is: ")
        # If the banner contains an empty string but the connection went through

        if result == "" or None:
            print("Banner not showing up :(")
            sock.close()
        else:
            print(('Banner is {}'.format(str(result))))
            sock.close()
            return result
    except IOError as error:
        sock.settimeout(5.0)
        if sock == socket.error:
            print("Making the socket didn't work :(")
        print(("Exception", error))
    finally:
        sock.close()
