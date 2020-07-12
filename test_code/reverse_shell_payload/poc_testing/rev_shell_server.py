''' This program listens on a port on this machine (Attacker) and waits for the client to connect back. Once the connection comes in. The shell initiates '''
import socket
import sys

''' Locally bind a socket to port so it can receive data '''
def listen_sock(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
    except socket.error as msg:
        sys.exit("Error: {}\nBind failed. Pagan...".format(msg))
    
    print("Binding is done")
    listen_conns = s.listen(1)
    print("Listening connections: {}".format(listen_conns))
    print('Socket is listening... on port {}'.format(port))
    # Wait infinitely
    while 1:
        conn, addr = s.accept()
        print("Connected: {}".format(addr))
        ''' No command handler available on the listener '''

    #s.close()

    return cmd

def main():
    port = int(sys.argv[1])
    listen_sock(port)

main()
