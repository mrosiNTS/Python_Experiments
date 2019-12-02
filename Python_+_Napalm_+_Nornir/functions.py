#!/usr/bin/env python3

import yaml
import json
import sys
import csv
from netaddr import *
from netmiko import ConnectHandler
from pprint import pprint

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

    groups.update ({'cisco_ios' : {'platform' : 'ios', 'connection_options' : {'napalm' : {'extras' : {'optional_args' : {'secret' : 'cisco'}}}}}})
    
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

def ssh(mgmt_IP, log_username, log_passw, en_passw):

    # accessing ssh to devices

    device = {
        'device_type': 'cisco_ios',
        'ip': mgmt_IP,
        'username': log_username,
        'password': log_passw,
        'secret': en_passw,
    }
    return device

def configure_lldp_on_device (device, login_user, login_passw, enable_passw):

    # open in reading the hosts.yaml file to get the ip address

    with open("hosts.yaml", "r") as file:

        try:
            config = yaml.safe_load(file)
        except Exception as err:
            print ('missing yaml file or wrong name')
            sys.exit()

    mgmt_IP_add = (config[device])['hostname']

    # configure lldp on global config and on interfaces

    device = ssh (mgmt_IP_add, login_user, login_passw, enable_passw)
    connection = ConnectHandler(**device)
    connection.enable()

    commands_global = ['lldp run']
    
    commands_interface = ['interface range gigabitEthernet 0/1 - 3', 'lldp transmit', 'lldp receive']
    
    # commit the global config command

    config_committed = connection.send_config_set(commands_global)

    # commit the interfaces commands

    config_committed = connection.send_config_set(commands_interface)

def write_interfaces_to_csv (out):

    #write on a .csv file the interfaces read from devices

    interf = {}

    with open ('./interfaces_facts.csv', 'w', newline = '') as file:

        # 'items' MUST have the same name of the "values" in the dictionary to be written in .csv file

        items = ['device', 'interface', 'is_enabled', 'is_up', 'description', 'mac_address', 'last_flapped', 'mtu', 'speed']
        int_facts = csv.DictWriter(file, fieldnames = items)
        int_facts.writeheader()

        for key, value in out.items():
            interf = (value[0].result)['interfaces']
            for int_key in interf:
                int_value = interf[int_key]
                router_interface = {'device': key, 'interface': int_key}
                router_interface.update(int_value)
                int_facts.writerow (router_interface)

def write_file_json(out):

    #write a json file with data from a list

    json_data = {}

    for key, value in out.items():
        print ('from ' + key + ':')
        neighbors = (value[0].result)['lldp_neighbors']
        print()

        json_data[key] = []
        for key_device in neighbors:
            json_data[key].append({
                'Local_Interface': key_device,
                'Remote_Router': (neighbors[key_device][0]['hostname']).replace('.cisco',''),
                'Remote_Interface': neighbors[key_device][0]['port']
            }) 

    with open('./json_data.json', 'w') as outfile:
        json.dump(json_data, outfile)

def read_file_json(file_json):

    with open(file_json, 'r') as infile:
        json_data = json.load(infile)

        for key, value in json_data.items():
            print ('Local Router: ' + key)
            print ()
            for list_obj in value:
                for key2, value2 in list_obj.items():
                    print(key2 + ' : ' + value2)    
            print()
