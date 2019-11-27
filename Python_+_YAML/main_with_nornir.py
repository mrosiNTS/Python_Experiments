#!/usr/bin/env python3

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from time import perf_counter
import sys
from functions import read_file
from functions import yaml_files_creation

def main():

	# Setting of IP subnet and username/password
	
	mgmt_IP_add, login_username, login_password, enable_password = read_file()

	# Creation yaml files

	yaml_files_creation (number_devices, mgmt_IP_add, login_username, login_password)

	# Normir for parallel execution of Netmiko

	nr = InitNornir(config_file="./config.yaml")
	
	start_time = perf_counter()
	output = []

	# all the SSH sessions and netmiko commands are executed in paralle on all the devices
	# the tests shown that instead of 26sec the process required 6sec to be executed on 4 routers
	
	output = nr.run(task=netmiko_send_command, command_string="show ip int b")

	for key, value in output.items():
		print ('from ' + key + ':')
		print ()
		print (value[0].result)
		print ()
	
	# as alternative to the previous while loop you can use this one:
	# print_result (output)

	end_time = perf_counter()
	total_time = end_time - start_time
	print ()
	print (f'TOTAL_TIME without parallelization: {total_time} sec')
	print ()

if __name__ == '__main__':

	# the argv[] in input are the less significative byte of IP mgmt address

	number_devices = len(sys.argv)-1

	if number_devices == 0:
		print('Last byte for at least one device has to be provided')
		sys.exit(1)

	main()


