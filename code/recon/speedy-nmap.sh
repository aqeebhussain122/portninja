#!/bin/bash
# Create a time array of elements
timeArr=()
# Make requests to a number of targets
# Make 4 pings when it's one target, make 1 when it's multiple. 
timeVals=$(for i in `cat target.txt`; do ping -c 2 -W 1 $i | grep ttl | awk {'print $7'} | grep -Eo '[0-9]{1,10}'; done)

# Cycle through the time values
for i in $timeVals; 
do 
	#echo $i;
	# Append each value to an array
	timeArr+=($i)
done

echo $timeVals
# Get the number of time values from the array
numElements=$(echo ${timeArr[@]} | tr ' ' '\n' | wc -l)
echo "There are $numElements elements in the array"

# Perform a bubble sort on all of these values - https://www.delftstack.com/howto/linux/bash-sort-array/
for ((i = 0; i<$numElements; i++))
do

	for((j = 0; j<$numElements-i-1; j++))
		do

			if [ ${timeArr[j]} -gt ${timeArr[$((j+1))]} ]
			then
				
				#swap
				temp=${timeArr[j]}
				timeArr[$j]=${timeArr[$((j+1))]}
				timeArr[$((j+1))]=$temp
			fi
		done
done

# Sorted array 
echo "Sorted array"
echo ${timeArr[*]}

minRttVal=${timeArr[0]}
maxRttVal=${timeArr[0 - 1]}

minRttValSum=$(($minRttVal + 25))
maxRttValSum=$(($maxRttVal + 100 ))

nmap -vvv -Pn -sS --min-rtt-timeout ${minRttValSum}ms --max-rtt-timeout ${maxRttValSum}ms --max-retries 1 --max-scan-delay 0 --min-hostgroup 4 -iL target.txt -oA Tuned_FullPort
