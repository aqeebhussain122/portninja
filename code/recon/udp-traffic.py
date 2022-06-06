from scapy.all import *
import sys
import datetime
import os
import time
from signal import signal, SIGINT

# Sniff UDP traffic to uncover ports on the network which are being reported as filtered by NMAP.

# Reference
#https://stackoverflow.com/questions/58410927/how-can-i-retrieve-a-packet-payload-as-a-bytearray-in-scapy

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
            udp_pkts = sniff(filter="udp", iface=target_interface, timeout=10)
            # Take all the packets in pkts variable as one by one element for loop.
            for udp_pkt in udp_pkts:
                # If a destination unreachable message is received
                # Write this to a local PCAP for further analysis.
                packet = bytes(udp_pkt[UDP].payload)
                packet_len = len(packet)
                if packet_len != 0:
                    print(packet)
                    print("Target UDP port: {}".format(udp_pkt[UDP].dport))
                    write_file =  wrpcap('udp-traffic.pcap', udp_pkt, append=True)
                else:
                    continue
                # Print out the IP address which reported rejected rules back.
                print("UDP traffic found from: {}".format(udp_pkt[IP].dst))

    except KeyboardInterrupt:
        sys.exit(0)


    return 0

if __name__ == '__main__':
    main()
