import ports
import sys

def scan_http(ip_addr):
    # Using these to check if the ports are open or not
    ports_open = 0
    ports_not_open = 0
    
    http_port_80 = 80 # Just numbers
    http_port_88 = 88
    http_port_443 = 443
    http_port_8080 = 8080
    #http_ports = [80,88,443,8080]
    http_ports = [http_port_80,http_port_88,http_port_443,http_port_8080]
    # error_exit = 0
    for port in http_ports:
        # Grabs the exit code of the function - 0 = success, 111 = error
        result = ports.TCPportCheck(ip_addr, port)
        if(result == 0):
            # Add in another list which associates to ports_open which can then be used for the requests
            ports_open += 1
        elif(result == 111):
            ports_not_open += 1

    return ports_open


def main():
    ip_addr = sys.argv[1]

    http_scan = scan_http(ip_addr)
    print("Target IP address: {}".format(ip_addr))
    if(http_scan == 0):
        print("[+] No HTTP ports found, shellshock module exiting... [+]")
        sys.exit(1)
    elif(http_scan != 0):
        print("Detected {} HTTP port(s) open \nLooking for cgi-bin....".format(http_scan))
    else:
        pass
    
main()
