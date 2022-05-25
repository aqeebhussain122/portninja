from scapy.all import *
import sys
import datetime
import os
import time
from signal import signal, SIGINT

# Sniff incoming ICMP code type 3 messages to enumerate REJECT firewall messages to spot internally open ports and misconfigured firewall

# Reference
#https://stackoverflow.com/questions/29801160/python-scapy-show-ip-of-the-ping-echo-requests

# If you send a ctrl + c to the sniffer, it will gracefully exit with an error message.
def signal_handler(signal, frame):
    print("\n[!] Sniffing ended [!]")
    # Exit code 0 because this is intended behavior
    sys.exit(0)

def main():
    # This can be tun0 or eth0, depending on where the ICMP response is going.
    target_interface = sys.argv[1]
    print("[!] Sniffing Started... [!]")

    try:
        # Prepare the SIGINT signal when you're ready to use it.
        signal(SIGINT, signal_handler)
        # The sniffer will not stop until manually stopped via ctrl + c
        while True:
            # Take all incoming packets and only sniff ICMP
            pkts = sniff(filter="icmp", iface=target_interface, timeout=10)
            # Take all the packets in pkts variable as one by one element for loop.
            for pkt in pkts:
                # If a destination unreachable message is received
                if str(pkt.getlayer(ICMP).type) == "3":
                    # Write this to a local PCAP for further analysis.
                    write_file =  wrpcap('firewall-reject-testing.pcap', pkt, append=True)
                    # Print out the IP address which reported rejected rules back.
                    print("Target Found: {}".format(pkt[IP].dst))

    except KeyboardInterrupt:
        sys.exit(0)


    return 0

if __name__ == '__main__':
    main()
