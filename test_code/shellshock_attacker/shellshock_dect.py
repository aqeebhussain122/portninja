import ports
import sys
import requests

'''
Authors: Aqeeb Hussain, Ben Gilhooley
Tool: Shellshock enum/attack
'''

def convert_list_to_string(input_list, sep):
    final_string = sep.join(input_list)
    return final_string

def get_status_code(ip_addr, port):
    cgi_url = extract_cgi_url(ip_addr, port)
    cgi_req = requests.get(cgi_url)
    cgi_req_status = cgi_req.status_code
    if(cgi_req_status == 403 or cgi_req_status == 301 or cgi_req_status == 200):
        print("cgi-bin is here")
    elif(cgi_req_status == 404):
        print("cgi-bin is not on the server, you got 404\nexiting....")
        sys.exit(1)
    else:
        pass
    return cgi_req_status

def extract_cgi_url(ip_addr, port):
    cgi_bin_exists = False
    https = True
    
    if port != 443:
        cgi_req_url_extract = requests.Request('GET', 'http://{}:{}/cgi-bin'.format(ip_addr,port))
        prep = cgi_req_url_extract.prepare()
        cgi_req_url = prep.url
    elif port == 443:
        cgi_req = requests.Request('GET', 'https://{}:{}/cgi-bin'.format(ip_addr, port))
        prep = cgi_req.prepare()
        cgi_url = prep.url
    else:
        pass
    return cgi_req_url

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

    
'''
Checks the wordlist and whichever words return 200, this function will return it
'''
def check_wordlist(ip_addr, port, word):
    base_url = extract_cgi_url(ip_addr, port)
    word_response = requests.get(base_url + '/' + word).status_code
    # Executes the wordlist 
    word_url_extract = requests.Request('GET', '{}/{}'.format(base_url, word))
    prep = word_url_extract.prepare()
    word_url = prep.url
    if(word_response == 200):
        print("cgi-bin target: {}".format(word_url))
    else:
        pass
    return word_response



def execute_wordlist(ip_addr, port, wordlist):
    found_urls = []

    base_url = extract_cgi_url(ip_addr, port)
    with open(wordlist) as file:
        # This reads the file
        words_to_check = file.read().strip().split('\n')
    
    print("Total words to check: {}".format(len(words_to_check)))
    for words in range(len(words_to_check)):
        word_response = requests.get(base_url + '/' + words_to_check[words]).status_code
        word_url_extract = requests.Request('GET', '{}/{}'.format(base_url,words_to_check[words]))
        prep = word_url_extract.prepare()
        word_url = prep.url
        if(word_response == 200):
            print("cgi-bin target(s) detected: {}".format(word_url))
            found_urls.append(word_url)


    return found_urls

def usage():
    if len(sys.argv) < 3:
        print("Arguments: <Target IP address> <wordlist>")
        sys.exit(1)

def main():
    usage()
    ip_addr = sys.argv[1]
    wordlist = sys.argv[2]
    print("Target IP address: {}".format(ip_addr))
    # Contains the open ports which are the return values from this function
    open_http_ports = scan_http(ip_addr)
    
    #open_ports_amount = len(http_scan)
    # Looping through by the number of open ports
    for port in range(len(open_http_ports)):
        print("Open HTTP ports are: {}".format(open_http_ports[port]))
        target_base_url = extract_cgi_url(ip_addr, open_http_ports[port])
        print("Target URL: {}".format(target_base_url))
        print("--------------------------------\nStarting cgi-bin directory detection")
        target_status_code = get_status_code(ip_addr, port)
        print("HTTP GET request status code of cgi-bin: {}".format(target_status_code))
        target_port = open_http_ports[port]
        print("The target port for cgi-bin detection is {}".format(target_port))
        print("--------------------------------\nStarting web crawler")
        print("Web crawler URL: {}".format(target_base_url))
        found_target_cgi_urls = execute_wordlist(ip_addr, port, wordlist)
        found_target_cgi_urls_str = convert_list_to_string(found_target_cgi_urls, '\n')
        print("Execute wordlist URL: {}".format(found_target_cgi_urls_str))
main()
