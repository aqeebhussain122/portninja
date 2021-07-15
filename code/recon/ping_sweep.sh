# Change the IP when needed
for i in 192.168.0.{1..254}; do
	ping -c 1 -W 1 "$i" &> /dev/null && echo "Host: $i is up"
done
