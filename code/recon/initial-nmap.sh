#!/bin/bash
check_root()
{
        if [ "$EUID" -ne 0 ]
          then 
          echo "Please run as root"
          exit
        fi
}

run_scan()
{
        # Scan the live hosts.
        sudo arp-scan -l | awk {'print $1'} 2>/dev/null | grep -i [0-9].[0-9] | sort -u > ips.txt
        # Get the live IPs, do host discovery and find the open ports only (backgrounded.)
        nmap -iL ips.txt --open -oA initial-tcp 2>&1 > /dev/null &
}

check_root
run_scan
