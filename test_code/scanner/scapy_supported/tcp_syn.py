import sys
from scapy.all import sr1, IP, TCP, ICMP
import random

def send_syn(target_ip, target_port):
    # Generate a raw packet on our side to send to the target 
    src_port = random.randint(1, 65535)

    resp_packet = sr1(IP(dst=target_ip)/TCP(sport=src_port, dport=int(target_port),flags="S"), timeout=2)
    # If a syn acknowledgement packet is recieved then it's open for sure

    ''' Error happening because port is coming back with an ICMP error, this can be further profiled with an ACK scan '''
    # IP / ICMP 192.168.59.130 > 192.168.59.129 dest-unreach port-unreachable / IPerror / TCPerror

    # The packet contained no data
    if(resp_packet == None):
        print('Port not processed: ', target_port)
        return resp_packet

    # If the packet has an ICMP layer, process it further
    if(resp_packet.haslayer(ICMP)):
        # Response packet gets ICMP layer then looks for the specific error codes which prevent it being processed because of a firewall
        if(int(resp_packet.getlayer(ICMP).type)==3 and int(resp_packet.getlayer(ICMP).code) in [1,2,3,9,10,13]):
            print("Filtered port: {} - Try an ACK scan".format(target_port))
            # return the state of the packet 
            return resp_packet

    # Packet returns a SYN/ACK packet resembling the port to be open
    if resp_packet.getlayer(TCP).flags == "SA":
        print(target_port, "is open")
        return resp_packet

    # An RST packet is sent back which means the port is definitely closed
    elif resp_packet.getlayer(TCP).flags == "RA":
        print(target_port, "is closed")
        return resp_packet
    else:
        pass
    return resp_packet

# Several returns are used so that the packet can be actively labelled with its state without errors

"""
def main():
    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    syn_packet = send_syn(target_ip, target_port)


#main() - Main included for individual testing
"""
