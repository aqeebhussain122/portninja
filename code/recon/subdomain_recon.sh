#!/bin/bash

###############################################
# Author(s): Aqeeb Hussain, Mattia Campagnano #
###############################################

check_amass_installed()
{
	amasspath=$(find / -type f -executable -name amass 2>/dev/null)
	for i in $amasspath
			do
				check_file=$(file $i | grep -i lsb | cut -d : -f 1)
			done

	check_ubuntu=$(uname -a | grep -iq ubuntu)
	ubuntu_exist=$?
	# If Amass is not installed.
	if [ -z "$check_file" ] ; then
		echo "Amass isn't installed. Attempting install on a Ubuntu OS."
		# Check if the installed system is Ubuntu. We don't need to see the output so we use -q
		if [ $ubuntu_exist -ne 0 ]; then
			# If Ubuntu is not installed then quit.
			echo "Your OS is not Ubuntu"			
			return 1
		else
			echo "OS is Ubuntu, downloading amass."
			download_amass=$(wget https://github.com/OWASP/Amass/releases/download/v3.19.2/amass_linux_amd64.zip -O ~/amass.zip)
			echo "Downloaded at: $(cd ~; pwd), unzipping: $(unzip ~/amass.zip)"
			# We only care about one result.
			find_amass=$(find ~ -type f -executable -name amass 2>/dev/null | tail -n 1)
			echo "Available at: $find_amass"
		fi
	fi
}

amass_scans()
{
#echo "Scanning for SSL cert/hostnames on given IP address/es"
#amass intel -active -addr $1 -timeout 1

	check_amass_installed

	find_amass=$(find / -type f -executable -name amass 2>/dev/null | tail -n 1)
	echo "Grabbing subdomains in passive mode"
	$find_amass enum -passive -d $1 -src

	echo "Grabbing further info in normal enum mode"
	$find_amass enum -d $1 -o "amassoutput"
}

root_domain=$1

echo "Performing subdomain checks via Wayback"
curl -s "http://web.archive.org/cdx/search/cdx?url=*.$1/*&output=text&fl=original&collapse=urlkey" |sort| sed -e 's_https*://__' -e "s/\/.*//" -e 's/:.*//' -e 's/^www\.//' | uniq

amass_scans $1
