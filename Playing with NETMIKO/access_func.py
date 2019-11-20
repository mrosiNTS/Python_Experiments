#!/usr/bin/env python3
from netmiko import Netmiko

def taskTOdo(FLAG, SHUTDOWN, INTERFACE, ADDRESS, MASK):

	net_connect = []

	cisco = {
		'host': '172.25.81.217',
		'username': 'cisco',
		'password': 'cisco',
		'device_type': 'cisco_ios',
		'secret': 'cisco', # passowrd per l'enable
   	}

	net_connect = Netmiko(**cisco)
	net_connect.enable()  # automatizza l'enable al login

	commands = []

	if FLAG in ['-m']:
		commands = ['interface vlan 1','no shutdown', 'ip address {0} {1}'.format(ADDRESS, MASK), 'exit']
	elif FLAG in ['-s']:
		commands = [INTERFACE,'shutdown', 'exit']
	elif FLAG in ['-a']:
		commands = [INTERFACE,'no shutdown', 'no switchport', 'ip address {0} {1}'.format(ADDRESS, MASK),'exit']
	
	net_connect.send_config_set(commands)
	net_connect.disconnect()
