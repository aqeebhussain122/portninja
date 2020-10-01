from scapy.all import *

def send_ack(ip, port, result = 1):
    src_port = RandShort()

    try: 
        p = IP(dst=ip)/TCP(sport=src_port, dport=port, flags='A', seq=65782)
        resp = sr1(p, timeout=2)
        # If no reply is sent back in the response then call it unreachable.
        if str(type(resp)) == "<type 'NoneType'>":
            result = 1

        # If the response as a TCP packet then 
        elif resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x4:
                result = 0
            elif (int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                result = 1

        if result == 0:
            print("Port {} is unfiltered".format(port))
        elif result == 1:
            print("Port {} is filtered".format(port))
        else:
            pass
    except Exception as e:
        pass
    return result

def main():
    target_ip = sys.argv[1]
    port = int(sys.argv[2])
    response = ack_scan(target_ip, port)

    return 0
#main()
