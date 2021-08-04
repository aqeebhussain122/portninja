#/usr/bin/python3
import sys
import subprocess
import re

###############################################
# Author(s): Aqeeb Hussain, Mattia Campagnano #
###############################################

def check_traceroute(traceroute_file):
    f = open(traceroute_file)
    lines = f.readlines()

    for line in lines:
        proc = subprocess.Popen(['traceroute', '{}'.format(line)], stdout=subprocess.PIPE)
        print(proc)



def check_ping(ping_file):
    f = open(ping_file, "r")
    lines = f.readlines()
    alive_hosts = []

    for line in lines:
        ip_addr = line.strip()
        proc = subprocess.Popen(['ping', '-c', '1', '{}'.format(ip_addr)], stdout=subprocess.PIPE)
        #print(proc)
        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
            print("Alive host: {}".format(ip_addr))
            output = stdout.decode()
            ttl = re.search('ttl=?\d+', output).group(0)
            found = "TTL for {} is: {} ".format(ip_addr, ttl)
            print(ttl)
            if "ttl=64" in ttl:
                print("OS is Linux")
            elif "ttl=128" or "ttl=127" in ttl:
                print("OS is Windows")
            alive_hosts.append(found)

    return alive_hosts


def main():
    # Make a dictionary which ties the IP addresses with its ttl value
 #   ip_ttl = {}

    filename = sys.argv[1]
    traced_hosts = check_traceroute(filename)
    """
    alive_hosts = check_ping(filename)
    print("\nDisplaying ttl values\n")
    for i in range(len(alive_hosts)):
        print(alive_hosts[i])
    """

main()
