# Take input from first command line argument and calculate the given number after /
# Limit the number selection from 1 to 32
# Map a specific amount of hosts to each value e.g. /30 = 2
# Maximum number of elements should be based upon the subnet number
# Store all subnet values in a list and map their values to an if condition


# Calculate the subnets in comparison to the number given using a hash
# Use hash in main function for ip address
#
def main():
    # Subnets stored in a hash function mixed with subnetting formula to distigiush hosts from the total addressing 
    subnets = {'/32': 1, '/31': 2, '/30': 4, '/29' : 8, '/28' : 16, '/27' : 32}
    print(subnets['/27'])

#def subnet_calc(ip_addr):


main()
