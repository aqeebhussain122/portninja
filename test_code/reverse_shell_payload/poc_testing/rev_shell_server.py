''' This program listens on a port on this machine (Attacker) and waits for the client to connect back. Once the connection comes in. The shell initiates '''
import socket
import sys

''' Locally bind a socket to port so it can receive data '''
def listen_sock(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
    except socket.error as msg:
        print(msg)
        print("Bind failed. Pagan...")
        sys.exit()
    print("Binding is done")
    
    listen_conns = s.listen(3)
    print("Listening connections: {}".format(listen_conns))
    print('Socket is listening...')
    # Wait infinitely
    while 1:
        conn, addr = s.accept()
        print("Connected")

    s.close()

    return addr

def main():
    port = int(sys.argv[1])
    listen_sock(port)

main()
