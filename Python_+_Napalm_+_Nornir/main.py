#!/usr/bin/env python3

from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from pprint import pprint
import sys
import json
from functions import read_file
from functions import yaml_files_creation
from functions import configure_lldp_on_device
from functions import write_interfaces_to_csv
from functions import write_file_json
from functions import read_file_json

def main():

	# Setting of IP subnet and username/password
	
	mgmt_IP_add, login_username, login_password, enable_password = read_file()

	# Creation yaml files

	yaml_files_creation (number_devices, mgmt_IP_add, login_username, login_password)

	# Normir for parallel execution of Napalm commands

	nr = InitNornir(config_file="./config.yaml")
	
	# collect interfaces configuration and write in excel file in .csv format

	output = []

	output = nr.run(task=napalm_get, getters=['interfaces'])

	write_interfaces_to_csv (output)

	# verify that LLDP is configured and if not, then configure it

	output = []

	lldp_run_command_ios = 'lldp run'

	output = nr.run(task=napalm_get, getters=['config'])

	for key, value in output.items():

		running_config = (((value[0].result)['config'])['running'])

		if lldp_run_command_ios not in running_config:
			print ("configuro lldp su " + key)
			configure_lldp_on_device (key, login_username, login_password, enable_password)
		else:
			print ("lldp e' configurato su " + key)

	# check the lldp neighbors and create the topology
		
	output = nr.run(task=napalm_get, getters=['lldp_neighbors'])

	# write on a json file the lldp topology

	write_file_json (output)

	# If i had to read from the previous json file the lldp topology and print in a human style i would have to call the module below

	read_file_json('./json_data.json')

if __name__ == '__main__':

	# the argv[] in input are the less significative byte of IP mgmt address

	number_devices = len(sys.argv)-1

	if number_devices == 0:
		print('Last byte for at least one device has to be provided')
		sys.exit(1)

	main()


