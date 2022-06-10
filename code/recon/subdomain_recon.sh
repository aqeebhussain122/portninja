#!/bin/bash

###############################################
# Author(s): Aqeeb Hussain, Mattia Campagnano #
###############################################

check_amass_installed()
{
	amasspath=$(find / -name amass 2>/dev/null)
	for i in $amasspath
			do
					check_file=$(file $i | grep -i lsb | cut -d : -f 1)
			done

	check_amass_installed=$?

	if [ $check_amass_installed -ne 0 ]; then
			echo "Amass is not there..."
			# If 1 is returned from the function, then try another function which tries to install amass on the system.
			return 1
	else
			# This value is returned from the function if all goes well.
			echo "$check_file"
	fi
}

amass_scans()
{
#echo "Scanning for SSL cert/hostnames on given IP address/es"
#amass intel -active -addr $1 -timeout 1

check_file=$(check_amass_installed)

echo "Grabbing subdomains in passive mode"
$check_file enum -passive -d $1 -src

echo "Grabbing further info in normal enum mode"
$check_file enum -d $1 -o "amassoutput"
}

root_domain=$1

echo "Performing subdomain checks via Wayback"
curl -s "http://web.archive.org/cdx/search/cdx?url=*.$1/*&output=text&fl=original&collapse=urlkey" |sort| sed -e 's_https*://__' -e "s/\/.*//" -e 's/:.*//' -e 's/^www\.//' | uniq

amass_installed=$(check_amass_installed)
echo $amass_installed

amass_scans $1
