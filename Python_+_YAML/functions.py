#!/usr/bin/env python3

import yaml
import sys
from netaddr import *

def read_file():

	# Reading config.yaml file

    with open("entry_config.yaml", "r") as file:
        try:
            config = yaml.safe_load(file)
        except Exception as err:
            print ('missing yaml file or wrong name')
            sys.exit()

    mgmt_IP_add = config["IP_add_subnet"]
    login_username = config["username"]
    login_password = config["password"]
    enable_password = config["enapassword"]
    return mgmt_IP_add, login_username, login_password, enable_password

#def ssh(mgmt_IP, log_username, log_passw, en_passw):

    # accessing ssh to devices

#    device = {
#        'device_type': 'cisco_ios',
#        'ip': mgmt_IP,
#        'username': log_username,
#        'password': log_passw,
#        'secret': en_passw,
#    }
#    return device

def yaml_files_creation (num_devices, mgmt_IP, login_user, login_passw):

    # dictionaries creation

    arg_count = 1
    hosts = {}
    groups = {}
    defaults = {}

    while arg_count < (num_devices+1):

        last_byte = int(sys.argv[arg_count])
        prefix = IPNetwork(mgmt_IP)
        add = str(prefix.network + last_byte)
        hosts.update ({'Router' + str(arg_count) : {'hostname' : add, 'groups' : ['cisco_ios']}}) 
        arg_count +=1

    groups.update ({'cisco_ios' : {'platform' : 'ios'}})

    defaults.update ({'username' : login_user}) 
    defaults.update ({'password' : login_passw})

    # create hosts, groups and defaults yaml files

    with open (r'./hosts.yaml', 'w') as file:
        file.write('---\n')
        hosts = yaml.dump(hosts, file)

    with open (r'./groups.yaml', 'w') as file:
        file.write('---\n')
        groups = yaml.dump(groups, file)

    with open (r'./defaults.yaml', 'w') as file:
        file.write('---\n')
        defaults = yaml.dump(defaults, file)