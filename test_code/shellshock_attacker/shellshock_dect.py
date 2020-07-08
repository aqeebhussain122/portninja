import ports
import sys

def scan_http(ip_addr):
    # Using these to check if the ports are open or not
    ports_open = 0
    ports_not_open = 0
    
    http_port_80 = 80 # Just numbers
    http_port_88 = 88
    http_port_443 = 443
    http_port_8080 = 8080
    #http_ports = [80,88,443,8080]
    http_ports = [http_port_80,http_port_88,http_port_443,http_port_8080]
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
            ports_open += 1
        elif(result == 111):
            ports_not_open += 1


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
    print(single_check)
    print(single_check_1)
    print(single_check_2)
    '''
    # END OF FOR LOOP
    # return ip_addr
    return ports_open
    #return error_exit

#def cgi_bin_detector(url, port):

def main():
    # This is the output of the IP address, not the function return
    #http_scan = scan_http("192.168.0.100")
    ip_addr = sys.argv[1]

    http_scan = scan_http(ip_addr)
    print("Target IP address: {}".format(ip_addr))
    if(http_scan == 0):
        print("[+] No HTTP ports found, shellshock module exiting... [+]")
        sys.exit(1)
    elif(http_scan != 0):
        print("Detected {} HTTP port(s) open \nLooking for cgi-bin....".format(http_scan))
    else:
        pass
    #This segment now works and we now need to send a request to the server with the 
    

    '''
    We want the return code of http_scan to proceed accordingly.
    By extracting the ports_open counter and measuring the if/else logic of 0 http ports being open
    then the program should exit from trying to identify the presence of a cgi-bin directory.
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
