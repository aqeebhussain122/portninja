import ports
import sys
import requests

'''
Make an HTTP request to the available ports and append /cgi-bin and get the return code of it
'''

'''
We need to get the status code based on the url and then if the code is 403 then proceed else if it's 404 then exit
Return the cgi request status code to main
'''
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

'''
Extract the target's URL from the HTTP GET request and return it to main
'''
def extract_cgi_url(ip_addr, port):
    '''
    Booleans used for future use
    '''
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

    
'''
Checks the wordlist and whichever words return 200, this function will return it
'''
def check_wordlist(ip_addr, port, word):
    base_url = extract_cgi_url(ip_addr, port)
    word_response = requests.get(base_url + '/' + word).status_code
    #word_url = requests.get(base_url + '/' + word)
    # Executes the wordlist 
    word_url_extract = requests.Request('GET', '{}/{}'.format(base_url, word))
    prep = word_url_extract.prepare()
    word_url = prep.url
    #print("CheckPath function output: {}".format(cgi_crawler.checkPath(cgi_target_url)))
    #print(word_url_extract)
    #print(word_url)
    if(word_response == 200):
        print("cgi-bin target: {}".format(word_url))
    else:
        pass
        #print("Nothing found")
        #sys.exit(1)
    return word_response



def execute_wordlist(ip_addr, port, wordlist):
    '''
    1. Open the file
    2. Read the file and check how many lines to check
    3. Open the for loop properly in which the crafted url can use the check_wordlist to see if a 200 entry appears
    4. (Do error handling of everything once the core code is written
    '''

    ''' SO FAR JUST A STATIC LINK IS CREATED IT SEEMS! '''
    base_url = extract_cgi_url(ip_addr, port)
    with open(wordlist) as file:
        # This reads the file
        words_to_check = file.read().strip().split('\n')
    print("Total words to check: {}".format(len(words_to_check)))
    for words in range(len(words_to_check)):
        word_response = requests.get(base_url + '/' + words_to_check[words])
        word_url_extract = requests.Request('GET', '{}/{}'.format(base_url,words_to_check[words]))
        prep = word_url_extract.prepare()
        word_url = prep.url
        print(word_url)
        print(word_response)
        '''
        This test just didn't even work...
        if(word_response == 200):
            print("Found: {}".format(word_url))
            sys.exit(0)
        '''

    '''
    Or this one
    if(word_response == 200):
        print("Found: {}".format)
    '''
        #print(check_wordlist(ip_addr, port, words_to_check[words]))
        # Print the words from the list first and then try to make a GET request in this 
        #print(words_to_check[words])
        # This prints the actual words in the wordlist
        #check_words = check_wordlist(ip_addr, port, words_to_check[word])
        #print(check_words)
        #print(word_url)
    return word_response


def main():
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
        target_status_code = get_status_code(ip_addr, port)
        print("HTTP GET Request status code: {}".format(target_status_code))
        target_port = open_http_ports[port]
        print("The target port for cgi-bin detection is {}".format(target_port))
        print("--------------------------------\nStarting web crawler")
        print("Web crawler URL: {}".format(target_base_url))
        #target_wordlist_response_code = check_wordlist(ip_addr, port, wordlist)
        #target_wordlist_response_code = check_wordlist(ip_addr, port, wordlist)
        #target_wordlist_response_code = check_wordlist(ip_addr, port, 'statu')
        #print("Wordlist checker response code: {}".format(target_wordlist_response_code))
        
        print("Execute wordlist URL: {}".format(execute_wordlist(ip_addr, port, wordlist)))
main()
