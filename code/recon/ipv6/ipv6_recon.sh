#!/bin/sh

interface_name=$1
filename=$2

args() 
{
	if [[ $# -ne 2 ]]
	then
		echo "Invalid number of arguments supplied. Usage: <Physical Interface Name> <Output file name>" && exit 1
	fi
}

ipv6_ssh_probes() 
{
	# Make a link local call to all hosts on the internal network
	scan_ipv6=`ping6 -I $1 -c 2 ff02::1 | grep DUP | awk '{print substr($4, 1, length($4)-1)}'`
	# Show all ipv6 neighbours found 
	show_ipv6_neighbours=`ip neigh show | grep fe80 | awk '{print $1 " " $5}' > $2`
	open_file=`cat $2`
	printf "Printing results...\n$open_file\n"
	
	while read line; do
		# We want to do something with each line
		ipv6=$(awk {'print $1'} <<< "$line")
		#echo $ipv6
		# Send one ping to the target and if it is alive then echo it
		ping_target=`ping6 -c 1 $ipv6%$interface_name | grep ttl`
		# Banner grabs the SSh version on the target with a timeout switch
		port_scan=`timeout 1 cat < /dev/tcp/$ipv6%$1/22`
		echo "Device $ipv6 has SSH version: $port_scan"
		# Using this to check for password based IPv6 entry points to try and crack them via IPv6
	done < $filename
}

args "$@"
ipv6_ssh_probes $1 $2
