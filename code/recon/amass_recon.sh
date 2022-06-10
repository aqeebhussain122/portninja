#!/bin/bash

###############################################
# Author(s): Aqeeb Hussain, Mattia Campagnano #
###############################################

amasspath=$(find / -name amass 2>/dev/null)
for i in $amasspath
        do
                check_file=$(file $i | grep -i lsb | cut -d : -f 1)
        done

check_amass_installed=$?

if [ $check_amass_installed -ne 0 ]; then
        echo "Amass is not there..."
        # If 1 is returned from the function, skip, else run amass scan. 
        return 1
else
        echo "Amass is installed, proceeding..."
fi

#echo "Scanning for SSL cert/hostnames on given IP address/es"
#amass intel -active -addr $1 -timeout 1

echo "Grabbing subdomains in passive mode"
$check_file enum -passive -d nmap.org -src

echo "Grabbing further info in normal enum mode"
$check_file enum -d nmap.org -o "amassoutput"
