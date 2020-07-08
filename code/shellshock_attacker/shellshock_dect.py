import ports
import sys

'''
Use an internal HTTP list of ports which will be scanned for being open/closed with 1 and 0
'''
def scan_http(ip_addr):
    # Using these to check how many ports are open/closed
    ports_open = 0
    ports_not_open = 0
   
    http_ports = (80,88,443,8080)
    # Sublists for the open and closed ports
    #http_open_ports = []
    http_open_ports = []
    http_closed_ports = []

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
        
    return http_open_ports


#def cgi_bin_detector(url, port):

def main():
    # IP address is separate variable instead of being part 
    ip_addr = sys.argv[1]

    # Contains the open ports which are the return values from this function
    http_scan = scan_http(ip_addr)
    print("Target IP address: {}".format(ip_addr))

main()
