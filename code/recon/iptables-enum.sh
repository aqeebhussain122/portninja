#!/bin/bash

# IP address and port need to be hardcoded
timeout 1 bash -c 'cat < /dev/null > /dev/tcp/$ip/$port'

code=$?
if [ $code -eq 124 ]; then
        echo "IPTables is likely applied on the specified port"
elif [ $code -eq 1 ]; then
        echo "Port is just closed, move on..."
elif [ $code -eq 0 ]; then
        echo "Port is open"
else
        echo "I have no idea about this code..."
fi
