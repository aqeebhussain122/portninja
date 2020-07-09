import sys
import requests
import socket

def usage():
    if len(sys.argv) < 3:
        print("Arguments: (Remote host, port, wordlist)")
        sys.exit(1)

def validate_host(remote_host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        status = sock.connect_ex((remote_host, int(port)))
        sock.close()
        # If the port is open
        if status == 0:
            print("Successful")
        else:
            print("Error: Host {} cannot be reached\n".format(remote_host))
            sys.exit(1)
    except socket.error:
        print("Error: Host {} cannot be reached\n".format(remote_host))
        sys.exit(1)

def validate_wordlist(wordlist, remote_host):
    try:
        with open(wordlist) as file:
            to_check = file.read().strip().split('\n')
        print("Total paths to check: {}".format(len(to_check)))
        for i in range(len(to_check)):
            checkPath(to_check[i], remote_host)
    except KeyboardInterrupt:
        print('\n[!] Error: Interrupted scan')
        sys.exit(1)
    except IOError:
        print('[!] Error: Failed to read file..\n')
        sys.exit(1)

def checkPath(path, remote_host):
    try:
        response = requests.get('http://' + remote_host + '/' + path).status_code
    except Exception:
        print ('[!] An error occured')
        sys.exit(1)
    if response == 200:
        print("Found: /{}".format(path))
    return response

def main():
    remote_host = sys.argv[1]
    port = sys.argv[2]
    wordlist = sys.argv[3]
    validate_host(remote_host, port)
    validate_wordlist(wordlist, remote_host)
    
    print ("Starting scan")
    # to_check = The variable which will check the paths
    print('\n[*] Scan complete')
main()
