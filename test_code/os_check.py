import os

def OScheck():
	if os.name == 'nt':
		print('The OS running is windows')
	else:
		print('The OS is not windows')
