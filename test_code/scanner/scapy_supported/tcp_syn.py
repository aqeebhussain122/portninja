import sys
from scapy.all import sr1, IP, TCP
import random

def send_syn(target_ip, port):
    # Generate a raw packet on our side to send to the target 
    src_port = random.randint(1, 65535)
    packet = sr1(IP(dst=target_ip)/TCP(sport=src_port, dport=int(port),flags="S"))
    # If a syn acknowledgement packet is recieved then it's open for sure
    if packet.getlayer(TCP).flags == "SA":
        print(port, "is open")
    
    return packet

def send_fin():
    return


def main():
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    syn_packet = send_syn(target_ip, target_port)
    print(syn_packet)

    packet_summary = syn_packet.summary( lambda s,r: r.sprintf("%TCP.sport% \t %TCP.flags%"))
    print(packet_summary)
main()
