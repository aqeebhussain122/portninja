#/usr/bin/python3
import sys
import subprocess
import re

def check_ping(ping_file):
    f = open(ping_file, "r")
    lines = f.readlines()

    traceroute_value = []
    trace_ttl = []
    for line in lines:
        ip_addr = line.strip()
        ping_proc = subprocess.Popen(['ping', '-c', '1', '{}'.format(ip_addr)], stdout=subprocess.PIPE)
    
        ping_stdout, ping_stderr = ping_proc.communicate()
        if ping_proc.returncode == 0:
            output = ping_stdout.decode()
            ttl = re.search('ttl=?\d+', output).group(0)
            ttl_value = re.search(r'\d+', ttl).group(0)
            ttl_value_int = int(ttl_value)

        elif ping_proc.returncode != 0:
            print("{} is not responding to pings".format(ip_addr))
            continue

        traceroute_proc = subprocess.Popen(['traceroute', '{}'.format(ip_addr)], stdout=subprocess.PIPE)
        traceroute_stdout, traceroute_stderr = traceroute_proc.communicate()
        if traceroute_proc.returncode == 0:
            output = traceroute_stdout.decode().split('\n')
            traceroute_value.append(output[-2][1])

        ttl_org = int(output[-2][1]) + ttl_value_int
        print("IP address: {} has original TTL of {}".format(ip_addr, ttl_org))
        trace_ttl.append([ip_addr, ttl_org])

    return trace_ttl

def main():
    filename = sys.argv[1]
    alive_hosts = check_ping(filename)
    for i in range(len(alive_hosts)):
        ttl_values = alive_hosts[i][1]
        #print(ttl_values)
        if ttl_values in range(50, 66):
            print("{} is Linux".format(alive_hosts[i][0]))
        elif ttl_values in range(120,129):
            print("{} is Windows".format(alive_hosts[i][0]))

main()
