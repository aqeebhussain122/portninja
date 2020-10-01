from scapy.all import ICMP, sr1, IP
import sys

# Perform an ICMP ping to see if the target is alive or not
def icmp_check(target_ip):
    icmp_send = IP(dst=target_ip)/ICMP()
    resp = sr1(icmp_send, timeout=1)
    if resp == None:
        print("Host unreachable")
        sys.exit(1)
        return False
    else:
        print("Host is reachable with ICMP ping")
        return True

    return resp
