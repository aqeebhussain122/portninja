import socket
import sys

'''
    Run this program on the target side which will be serving a file from a Python socket
'''

host = sys.argv[1]
port = int(sys.argv[2])
send_file = sys.argv[3]

print("Socket listening on: {}:{}".format(host, port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(5)
    s.bind((host, port))
    s.listen()

    # Payload wrapped into a true loop waiting for connection to be accepted
    while True:
        conn, addr = s.accept()
        print('Incoming connection from: ', addr)
        data = conn.recv(1024)
        # File you're going to read data 
        filename = send_file
        f = open(filename, 'rb')
        read = f.read(1024)
        while(read):
            conn.send(read)
            print('Sent', repr(read))
            read = f.read(1024)
        f.close()

        print("Send finished")
        conn.send(b"Connection ended")
        conn.close()
        s.settimeout(None)
        # Kill the connection once the data is received
        break
