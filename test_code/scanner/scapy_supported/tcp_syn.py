import sys
from scapy.all import sr1, IP, TCP, ICMP
import random

def send_syn(target_ip, port):
    # Generate a raw packet on our side to send to the target 
    src_port = random.randint(1, 65535)

    resp_packet = sr1(IP(dst=target_ip)/TCP(sport=src_port, dport=int(port),flags="S"), timeout=2)
    # If a syn acknowledgement packet is recieved then it's open for sure

    ''' Error happening because port is coming back with an ICMP error, this can be further profiled with an ACK scan '''
    # IP / ICMP 192.168.59.130 > 192.168.59.129 dest-unreach port-unreachable / IPerror / TCPerror
    ''' Put this in a try catch because function is only syn scan and should not be bothered by other things other than what a SYN scan entails '''
    
    if(resp_packet.haslayer(ICMP)):
        # Think of a better way to present this
        if(int(resp_packet.getlayer(ICMP).type)==3 and int(resp_packet.getlayer(ICMP).code) in [1,2,3,9,10,13]):
            print("Filtered port - Try an ACK scan")
            sys.exit(1)

    if resp_packet.getlayer(TCP).flags == "SA":
        print(port, "is open")
    elif resp_packet.getlayer(TCP).flags == "RA":
        print(port, "is closed")
    else:
        pass
    return resp_packet
    
#def send_fin():
#    return


def main():
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    syn_packet = send_syn(target_ip, target_port)

    #packet_summary = syn_packet.summary( lambda s,r: r.sprintf("%TCP.sport% \t %TCP.flags%"))
    #print(packet_summary)
#main()
