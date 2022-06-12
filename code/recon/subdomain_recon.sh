#!/bin/bash

###############################################
# Author(s): Aqeeb Hussain, Mattia Campagnano #
###############################################


# Check if amass is installed or not to determine installation.
check_amass_installed()
{
	amasspath=$(find / -type f -executable -name amass 2>/dev/null)
	
	# Check if the system is Ubuntu	
	check_ubuntu=$(uname -a | grep -iq ubuntu)
	ubuntu_exist=$?
	# If Amass is not installed. Need to change this logic to cater for a source code installation via Go. 
	if [ -z "$check_file" ] ; then
		echo "Amass isn't installed. Attempting install on a Ubuntu OS."
		# Check if the installed system is Ubuntu. We don't need to see the output so we use -q
		if [ $ubuntu_exist -ne 0 ]; then
			# If Ubuntu is not installed then quit.
			echo "Your OS is not Ubuntu"
			return 1
		# If the OS is Ubuntu then download and install amass.
		else
			echo "OS is Ubuntu, downloading amass."
			download_amass=$(wget https://github.com/OWASP/Amass/releases/download/v3.19.2/amass_linux_amd64.zip -O ~/amass.zip)

			echo "Downloaded at: $(cd ~; pwd), unzipping: $(unzip ~/amass.zip)"
			# Find exact location of amass and then show this in a messagie
			find_amass=$(find ~ -type f -executable -name amass 2>/dev/null | tail -n 1)
			echo "Available at: $find_amass"
		fi
	fi
}

# Main function to conduct amass scans.
amass_scans()
{

	# Function to check if amass even installed.
	check_amass_installed

	# Grab a copy of amass from the file system to use in the script.
	find_amass=$(find / -type f -executable -name amass 2>/dev/null | tail -n 1)
	echo "Grabbing subdomains in passive mode"
	# Passively grab stuff, need to split this up using a switch of passive or aggressive.
	$find_amass enum -passive -d $1 -src

	# Enumerate normally and write to a file. 
	echo "Grabbing further info in normal enum mode"
	$find_amass enum -d $1 -o "amassoutput"

}

# The input parameter is the root domain. Need a usage function for this.
root_domain=$1

echo "Performing subdomain checks via Wayback"
# Do some enumeration via wayback
curl "http://web.archive.org/cdx/search/cdx?url=*.$root_domain/*&output=text&fl=original&collapse=urlkey" | sort | sed -e 's_https*://__' -e "s/\/.*//" -e 's/:.*//' -e 's/^www\.//' | uniq | tee -a wayback_domains.txt

echo "I found $(grep $1 wayback_domains.txt | wc -l) domains on wayback"

# Input parameter is the root doman to conduct the scans. 
amass_scans $root_domain
