from scapy.all import *

def send_ack(ip, port, result = 1):
    src_port = RandShort()

    try: 
        p = IP(dst=ip)/TCP(sport=src_port, dport=port, flags='A', seq=65782)
        resp = sr1(p, timeout=2)
        # If no reply is sent back in the response then call it unreachable.
        #if str(type(resp)) == "<type 'NoneType'>": - Inefficient
        #    result = 1
        if resp == None:
            result = 1

        # If the response as a TCP packet then 
        if resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x4:
                result = 0

        if resp.haslayer(ICMP):
            if (int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                result = 1
    except Exception as e:
        pass
    return result

def main():
    target_ip = sys.argv[1]
    port = int(sys.argv[2])
    response = ack_scan(target_ip, port)
    if response == 0:
        print("Port {} is unfiltered".format(port))
    elif response == 1:
        print("Port {} is filtered".format(port))
    else:
        pass
    print(response)
    return 0
#main()
