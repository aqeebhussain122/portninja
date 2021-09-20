import json
import sys

def read_json(json_harv_file):
    with open('{}'.format(json_harv_file), 'r') as json_file:
        data = json_file.read()
    
    obj = json.loads(data)
    if not json_harv_file:
        raise Exception("No file was provided")

    return obj

def json_hosts(json_harv_file):
    with open('{}'.format(json_harv_file), 'r') as json_file:
        data = json_file.read()

    obj = json.loads(data)
# Available keys
    print(obj.keys())

    hosts = obj['hosts']

    for i in range(len(hosts)):
        l = hosts[i].split(':')
        #print(l)
        hostnames = l[0]
        ip_addrs = l[1:]
        if not hostnames:
            print('No hostname found')
        elif not ip_addrs:
            print('No IP found for {}'.format(hostnames))
        
        print("Hostname(s): {} / IP address(es): {}".format(hostnames, str(ip_addrs)))


def json_emails(json_harv_file):

    obj = read_json(json_harv_file)
    if "emails" not in obj:
        print("No emails found")
    
    elif "emails" in obj:
        emails = obj['emails']
        for i in range(len(emails)):
            print(emails[i])
    
        # Insert email parsing here
    #print(emails)

def json_urls(json_harv_file):
    obj = read_json(json_harv_file)
    if "interesting_urls" not in obj:
        print("No URLs found")
    
    elif "interesting_urls" in obj:
        interesting_urls = obj['interesting_urls']
        for i in range(len(interesting_urls)):
            print(interesting_urls[i])


def json_asns(json_harv_file):
    obj = read_json(json_harv_file)
    if "asns" not in obj:
        print("No ASNs found")
    
    elif "asns" in obj:
        asns = obj['asns']
        for i in range(len(asns)):
            print(asns[i])

json_file = sys.argv[1]
print("Discovered URLs")
urls = json_urls(json_file)
print("\nDiscovered ASNs")
asns = json_asns(json_file)
print("\nDiscovered emails")
email = json_emails(json_file)
print("\nDiscovered hosts")
hosts = json_hosts(json_file)
