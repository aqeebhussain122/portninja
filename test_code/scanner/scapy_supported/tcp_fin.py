from scapy.all import *

def fin_scan(ip, port):
    src_port = RandShort()

    fin_scan_resp = sr1(IP(dst=ip)/TCP(sport=src_port, dport=port, flags='F', seq=65782),timeout=2)
    # If no reply is sent back in the response then call it unreachable.

    if fin_scan_resp == None:
        print("Open")
        return fin_scan_resp

    # If the response as a TCP packet then 
    if fin_scan_resp.haslayer(TCP):
        if fin_scan_resp.getlayer(TCP).flags == 0x14:
            print("Closed")
            return fin_scan_resp

    if fin_scan_resp.haslayer(ICMP):
        if(int(fin_scan_resp.getlayer(ICMP).type)==3 and int(fin_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
            print("filtered")
            return fin_scan_resp
        else:
            pass

    return fin_scan_resp

def main():
    target_ip = sys.argv[1]
    port = int(sys.argv[2])
    response = fin_scan(target_ip, port)
    return 0
main()
