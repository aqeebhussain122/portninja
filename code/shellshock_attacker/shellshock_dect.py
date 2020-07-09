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
    
    print("The target port for CGI function is {}".format(port))

    
    # If port not 443 then don't use an HTTPS query
    if port != 443:
        # Repository uses different modules so two calls are made to get the status code
        cgi_req_url_extract = requests.Request('GET', 'http://{}:{}/cgi-bin'.format(ip_addr,port))
        cgi_req = requests.request('GET', 'http://{}:{}/cgi-bin'.format(ip_addr,port))
        print("Status code: {} ".format(cgi_req.status_code))
        prep = cgi_req_url_extract.prepare()
        cgi_req_url = prep.url
        
        '''
        cgi_req_get = requests.get('http://{}:{}/cgi-bin'.format(ip_addr, port))
        cgi_req_response = cgi_req_get.status_code
        print(cgi_req_response)
        '''
        # That is the url with ip address as variable
        #print(cgi_req)
        #prep = cgi_req_url_extract.prepare()
        #cgi_req_url = prep.url
    '''
    else:
        cgi_req = requests.Request('GET', 'https://{}:{}/cgi-bin'.format(ip_addr, port)) 
        prep = cgi_req.prepare()
        cgi_url = prep.url
    '''
    return cgi_req_url

'''
Use an internal HTTP list of ports which will be scanned for being open/closed with 1 and 0
'''
def scan_http(ip_addr):
    # Using these to check how many ports are open/closed
    ports_open = 0
    ports_not_open = 0 

    http_ports = (80,88,443,8080)
    # Sublists for the open and closed ports
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

def main():
    ip_addr = sys.argv[1]
    print("Target IP address: {}".format(ip_addr))
    # Contains the open ports which are the return values from this function
    open_http_ports = scan_http(ip_addr)
    
    #open_ports_amount = len(http_scan)
    # Looping through by the number of open ports
    for port in range(len(open_http_ports)):
        print("Open HTTP ports are: {}".format(open_http_ports[port]))
        target_url = cgi_enum(ip_addr, open_http_ports[port])
        print("Target URL: {}".format(target_url))

main()
