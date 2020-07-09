import ports
import sys
import requests

'''
Make an HTTP request to the available ports and append /cgi-bin and get the return code of it
'''
def cgi_enum(ip_addr, port):
    '''
    Booleans used for future use
    '''
    cgi_bin_exists = False
    https = True
    '''
    1. Make an HTTP request to the given ip and port
    2. IP & port need to be variable
    '''
    print("The target port for CGI function is {}".format(port))
    # That is the url with ip address as variable

    # If port not 443 then don't use an HTTPS query
    '''
    if port != 443:
        # Do an HTTP query if not 443
        https = False
        cgi_req = requests.get('http://{}:{}/cgi-bin'.format(ip_addr,port))
    else:
        cgi_req = requests.get('https://{}:{}/cgi-bin'.format(ip_addr,port))
    '''
    if port != 443:
        cgi_req = requests.Request('GET', 'http://{}:{}/cgi-bin'.format(ip_addr,port))
        prep = cgi_req.prepare()
        cgi_url = prep.url
    else:
        cgi_req = requests.Request('GET', 'https://{}:{}/cgi-bin'.format(ip_addr, port)) 
        prep = cgi_req.prepare()
        cgi_url = prep.url

    '''
    #print("Request headers: \n\n {}".format(cgi_req.headers))
    #req_status_code = cgi_req.status_code
    '''

    '''
    if req_status_code == 403 or req_status_code == 200 or req_status_code == 301:
        cgi_bin_exists = True
        print("CGI-BIN status: {}".format(cgi_bin_exists))
    elif(req_status_code == 404):
        print("CGI-BIN not found")
        pass
    else:
        pass
    '''
    #print("Target server with CGI-BIN status is: {}".format(cgi_req))
    return cgi_url

'''
Use an internal HTTP list of ports which will be scanned for being open/closed with 1 and 0
'''
def scan_http(ip_addr):
    # Using these to check how many ports are open/closed
    ports_open = 0
    ports_not_open = 0
   
    '''
    Don't need these
    http_port_80 = 80 # Just numbers
    http_port_88 = 88
    http_port_443 = 443
    http_port_8080 = 8080
    '''

    '''
    These are the main http ports which need to be split to two more sublists of open_http_ports and closed_http_ports.
    This can be used further for processing in the other functions
    '''
    #http_ports = [80,88,443,8080]
    http_ports = (80,88,443,8080)
    # Sublists for the open and closed ports
    #http_open_ports = []
    http_open_ports = []
    http_closed_ports = []
    #http_ports = [http_port_80,http_port_88,http_port_443,http_port_8080]
    # error_exit = 0
    '''
    single_check = ports.TCPportCheck(ip_addr, 80)
    single_check_1 = ports.TCPportCheck(ip_addr, 8080)
    single_check_2 = ports.TCPportCheck(ip_addr, 88)
    if(single_check == 0):
        successful += 1
        print("successful value: {}".format(successful))
    if(single_check_1 == 111):
        not_successful += 1
        print("Not successful value: {}".format(not_successful))
    ''' 
    for port in http_ports:
        # Grabs the exit code of the function - 0 = success, 111 = error
        result = ports.TCPportCheck(ip_addr, port)
        if(result == 0):
            # Add in another list which associates to ports_open which can then be used for the requests
            # Currently only counters are placed to satisfy error conditions, no ports are being attached to the counters.
            ports_open += 1
            http_open_ports.append(port)
        elif(result == 111):
            ports_not_open += 1
            http_closed_ports.append(port)
        else:
            pass

    # If there's no open ports
    if not http_open_ports:
        print("No ports open, aight imma head out")
        sys.exit(1)
        '''
        Printing out the ports is pointless because ports.py does it 
        for i in range(len(http_open_ports)):
            print("Open: {}".format(http_open_ports[i]))
        
        for i in range(len(http_closed_ports)):
            print("Closed: {}".format(http_closed_ports[i]))
        '''

        '''
        string_http_open_ports = [str(open_ports) for open_ports in http_open_ports]
        # Replaced the [] with a space
        encoded_open_ports = ",".join(string_http_open_ports)
        string_http_closed_ports = [str(closed_ports) for closed_ports in http_closed_ports]
        encoded_closed_ports = ",".join(string_http_closed_ports)
        print("Open port(s) are {}".format(encoded_open_ports))
        print("Closed port(s) are: {}".format(encoded_closed_ports))
        '''
    # If the list is empty
        #print("Successful {}".format(successful))
        #print("Not successful {}".format(not_successful))

    #if(successful == 0):
        # Error section - If no ports are open then entire section just goes off
   #     print("Found no HTTP ports open, ima dip")
        #sys.exit(1) - Adding this exit code here causes the function to quit prematurely
        # Get the error_exit variable to be either 0 or 1 and return that 
        #print(error_exit)
        
    '''
    Trying to pull out the success codes of each port response
    using if statements with successful and not_successful, increment the variables and print them
    success = 0
    fail = 111
    '''

    '''
    rint(single_check)
    print(single_check_1)
    print(single_check_2)
    '''
    # This counter is to check for the 
    return http_open_ports
#
    # Return the list elements of an 
    #return error_exit

#def cgi_bin_detector(url, port):

def main():
    # IP address is separate variable instead of being part 
    ip_addr = sys.argv[1]
    print("Target IP address: {}".format(ip_addr))
    # Contains the open ports which are the return values from this function
    '''
    Get the open ports, make sure they're integers and then pass them through to the needed functions
    '''
    open_http_ports = scan_http(ip_addr)
    
    #open_ports_amount = len(http_scan)
    # Looping through by the number of open ports
    for port in range(len(open_http_ports)):
        print("Open HTTP ports are: {}".format(open_http_ports[port]))
        target_url = cgi_enum(ip_addr, open_http_ports[port])
        print("Target URL: {}".format(target_url))
        '''
        This will traverse through the list elements which are the port numbers
        The port numbers serve as parameters for the next function which is to detect cgi-bin
        http:// <- startswith (IP address):(port) <- append a /cgi-bin <- if this returns 403 or 200 then we're good to go with the crawling
        else if the program gives 404, just dip.
        cgi_bin_detector(ip_addr, open_http_ports[port])
        '''
        # Testing to see if it works with a function
        #ports.TCPportCheck(ip_addr, http_scan[port])

        # Testing to see if the list elements in http_scan can be treated as ports
        #ports.TCPportCheck(ip_addr, http_scan[i])

    #print("Function return: {}\nFunction data type: {}".format(http_scan, type(http_scan)))

    '''
    list to integer procedure (Maybe)
        1. Turn the list elements into strings
        . Turn the strings into ints
    '''
    # This if/else logic needs to be sorted out
    '''
    if(http_scan == 0):
        print("[+] No HTTP ports found, shellshock module exiting... [+]")
       #sys.exit(1)
    elif(http_scan != 0):
        print("Detected {} HTTP port(s) open \nLooking for cgi-bin....".format(http_scan))
    else:
        pass
    #This segment now works and we now need to send a request to the server with the  
    '''

    '''
    We want the return code of http_scan to proceed accordingly.
    By extracting the ports_open counter and measuring the if/else logic of 0 http ports being ope
    then the program should exit from trying to identify the presence of a cgi-bin directory.
    Instead of doing this between the function and main, it's better to contain all error handling in the function 
    '''
main()
        
#def main():
'''
import ports <- Contains all of the socket code
# Pre-populated ports
def scan_http(ip_addr)
(Scan of all the ports first)
# Network socket to scan 4 ports 
# Scan for 88, 80, 443 and 8080 see which one is open
ports = [80,88,443,8080]
for i in ports:
    (create 4 sockets with given IP and then populate ports from list)
    TCPPortCheck(ip_addr, 80)...
    The true/false elements of the array and try to count each of them
    if none of them are true then exit, else: continue
print(result of loop)

return ports

# Crawls the server on one of the ports
def cgi-bin-crawl(wordlist):
target_dir = "cgi-bin" <- May need some work lol
# How would we find cgi-bin???
if(target_dir == True):
else:
    print("cgi-bin not found")
'''

'''
def main():
    # If it's successful
    if(scan_http == 0):
        cgi_bin_crawl(wordlist)
        if(cgi_bin_crawl == 0):
            # Automated attack of shellshock - echo /etc/passwd
            shellshock_attack()
scan_http("192.168.0.102")
'''
