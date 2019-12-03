#!/usr/bin/env python3

from netmiko import ConnectHandler
from time import perf_counter
import sys
from netaddr import *
from functions import read_file
from functions import ssh


def main():

	# Setting of IP subnet and username/password
	
	mgmt_IP_add, login_username, login_password, enable_password = read_file()

	# SSH to devices
	# is assumed that the mask of mgmt >= 24

	arg_count = 1
	start_time = perf_counter()

	while arg_count < (number_devices+1):

		last_byte = int(sys.argv[arg_count])
		prefix = IPNetwork(mgmt_IP_add)
		add = str(prefix.network + last_byte)
		device = ssh (add, login_username, login_password, enable_password)
		connection = ConnectHandler(**device)
		connection.enable()
		output = connection.send_command("show ip int b")
		print (output)
		arg_count +=1

	end_time = perf_counter()
	total_time = end_time - start_time
	print ()
	print (f'TOTAL_TIME without parallelization: {total_time} sec')
	print ()

if __name__ == '__main__':

	number_devices = len(sys.argv)-1

	if number_devices == 0:
		print('Last byte for at least one device has to be provided')
		sys.exit(1)

	main()


