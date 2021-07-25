#/usr/bin/python3
import sys
import subprocess
import re

def check_ping(ping_file):
    f = open(ping_file, "r")
    lines = f.readlines()
    alive_hosts = []
    traceroute_value = []
    
    for line in lines:
        ip_addr = line.strip()
        ping_proc = subprocess.Popen(['ping', '-c', '1', '{}'.format(ip_addr)], stdout=subprocess.PIPE)
    
        ping_stdout, ping_stderr = ping_proc.communicate()
        if ping_proc.returncode == 0:
            output = ping_stdout.decode()
            ttl = re.search('ttl=?\d+', output).group(0)
            ttl_value = re.search(r'\d+', ttl).group(0)
            ttl_value_int = int(ttl_value)

        traceroute_proc = subprocess.Popen(['traceroute', '{}'.format(ip_addr)], stdout=subprocess.PIPE)
        traceroute_stdout, traceroute_stderr = traceroute_proc.communicate()
        if traceroute_proc.returncode == 0:
            output = traceroute_stdout.decode().split('\n')
            traceroute_value.append(output[-2][1])

        ttl_org = int(output[-2][1]) + ttl_value_int
        print("IP address: {} has original TTL of {}".format(ip_addr, ttl_org))

def main():
    filename = sys.argv[1]
    alive_hosts = check_ping(filename)

main()
