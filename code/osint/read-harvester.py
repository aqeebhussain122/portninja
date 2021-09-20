import json
import sys


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
    with open('{}'.format(json_harv_file), 'r') as json_file:
        data = json_file.read()

    obj = json.loads(data)
    if "emails" not in obj:
        print("No emails found")
    else:
        pass
        # Insert email parsing here
    #print(emails)

def json_urls(json_harv_file):
    with open('{}'.format(json_harv_file), 'r') as json_file:
        data = json_file.read()
        obj = json.loads(data)
        print(obj['asns'])
        if "interesting_urls" not in obj:
            print("No URLs found")
        
        interesting_urls = obj['interesting_urls']
        for i in range(len(interesting_urls)):
            print(interesting_urls[i])


def json_asns(json_harv_file):
    with open('{}'.format(json_harv_file), 'r') as json_file:
        data = json_file.read()
        obj = json.loads(data)
        if "asns" not in obj:
            print("No ASNs found")

        asns = obj['asns']
        for i in range(len(asns)):
            print(asns[i])

print("Discovered hosts")
json_hosts('harvester.json')
print("Discovered emails")
json_emails('harvester.json')
print("Discovered URLs")
urls = json_urls('harvester.json')
print("Discovered ASNs")
asns = json_asns('harvester.json')
