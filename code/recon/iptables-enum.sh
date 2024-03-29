#!/bin/bash

# IP address and port need to be hardcoded
#timeout 1 /bin/bash -c 'cat < /dev/null > /dev/tcp/192.168.1.11/8080'

ip=$1
port=$2

timeout 1 /bin/bash -c 'cat < /dev/null > /dev/tcp/192.168.0.56/810'

code=$?
echo "Error code is: $code"
if [ $code -eq 124 ]; then
        echo "IPTables is likely applied on the specified port"
elif [ $code -eq 1 ]; then
        echo "Port is just closed, move on..."
elif [ $code -eq 0 ]; then
        echo "Port is open"
else
        echo "I have no idea about this code..."
fi
