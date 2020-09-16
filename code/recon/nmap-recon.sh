### Single target identification for now ###
validate_ip() {
	local target_ip=$1

	if [[ $target_ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
		echo "IP address is $1"
	else
		echo "Usage: <Target IP address>"
		exit 1
	fi
}

ping_ip() {
	local target_ip=$1
	local ping_target=`ping -c 1 $target_ip`
	local ttl="$( ping -c 1 $target_ip | grep ttl | sed 's/.*ttl=\([[:digit:]]*\).*/\1/')"
	echo "Pinging IP: $1"
	if [ $? -eq 0 ]; then
		printf "Ping to $1: Successful \n\n"
	else
		echo "Ping to $1: Unsuccessful, host may be firewalled or inactive"
		#exit 1 - Error exit code
	fi
	# TTL is dependant upon the packet hops which are made from source to destination
	if [ $ttl == 64 ] || [ $ttl == 63 ]; then
		echo "OS is Linux"
	elif [ $ttl == 128 ] || [ $ttl == 127 ]; then
		echo "OS is Windows"
	else
		echo "Can't recognise OS from TTL value"
	fi
	echo $ttl
}

nmap_aggressive() {
	local target_ip=$1
	local target_dir="./nmap/$target_ip"
	local reg_scan=$1_regular_output
	local full_scan=$1_full_scan_output
	local detailed_scan=$1_detailed_scan_output
	echo "Creating workspace directory for nmap scans"
	#mkdir nmap
	if [ -d "$target_dir" ]; then
		echo "nmap directory exists"
		#exit 1
	else
		echo "Directory no existing lol, I'll create it now."
		mkdir -p -v "$target_dir"
	        echo "I made it"; ls nmap
	fi

	#if [ -d "./nmap/$target_ip" ]; then
	#	echo "IP workspace exists"
	#else
	#	echo "IP workspace don't exist"
	#fi
	# Relative path (So you can be anywhere on file system and this will unpack where you are
	cd "$target_dir"
	pwd
	echo "Performing regular nmap scan and outputting to file"
	nmap $1 -T4 -n  > $reg_scan
	if [ $? -eq 0 ]; then
		echo "File was made, printing it stdout now"
		cat $reg_scan
	else	
		echo "File wasn't created, some issue"
	fi
	echo "Performing full port scan "
	nmap $1 -T4 -p- -n > $full_scan
	cat $full_scan

	#grep tcp $full_scan | cut -d / -f 1 | tr '\n' ',' | sed 's/,$//'
	ports=`grep tcp $full_scan | cut -d / -f 1 | tr '\n' ',' | sed 's/,$//'`
	printf "Target ports to scan: $ports"
	printf "\n\n"
	printf "Running detailed scan"
	nmap -sT -sC -sV -T4 -n -p $ports $1 > $detailed_scan
	cat $detailed_scan
}


#validate_ip $1
ping_ip $1
#nmap_aggressive $1
