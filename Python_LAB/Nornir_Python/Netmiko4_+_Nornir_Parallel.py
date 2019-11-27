#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from __future__ import print_function, unicode_literals
from netmiko import ConnectHandler
from datetime import datetime
import time
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import netmiko_send_config

################## cleaning previous config ###########################

def clean_interface_config (devices):

    intf = 0
    num_max_interfaces = 2

    for intf in range(num_max_interfaces):
        Interface_commands = ['default interface gigabitEthernet 0/{0}'.format(intf), 'exit']
        devices.run(netmiko_send_config, config_commands=Interface_commands)

def clean_OSPF_config(devices):

    Interface_commands = ['no router ospf 10', 'exit']
    devices.run(netmiko_send_config, config_commands=Interface_commands)

################# deploying the new configuration ######################

def interface_config(devices):

    interface_0_0 = (devices.inventory.hosts["router1"])["interface_0_0"]
    interface_0_1 = (devices.inventory.hosts["router1"])["interface_0_1"]

    for intf in range(num_max_interfaces):
        Interface_commands = ['interface gigabitEthernet 0/{0}'.format(intf), 'no switchport', 'ip address {0} 255.255.255.252'.format(interface_0_0), 'no shutdown', 'exit']
        devices.run(netmiko_send_config, config_commands=Interface_commands)

def ospf_config(devices):
    
    OSPF_commands = ['configure terminal', 'router ospf 10', 'router-id {0}'.format(a_device['ip']), 'network 10.0.0.0 0.0.0.15 area 0', 'exit']
    devices.run(netmiko_send_config,config_commands=OSPF_commands)

###################### cheking configuration applied #####################

def check_int_config(devices):

    print()
    print(devices.run(netmiko_send_command, command_string="show ip interface brief"))
    print()
    print ("++++++++++++++++++++++++++ END ++++++++++++++++++++++++")
    print() 

def show_OSPF_adj(devices):

    print()
    print(devices.run(netmiko_send_command, command_string="show ip ospf neighbor"))
    print()
    print ("++++++++++++++++++++++++++ END ++++++++++++++++++++++++")
    print()

############################ main #########################################

def main():

    all_devices = InitNornir(config_file="config.yaml")
    router1 = all_devices.inventory.hosts["router1"]

    print(router1["host"])
    start_time = datetime.now()
    
# config cleaning (interfaces and OSPF)

    clean_interface_config (all_devices)
    clean_OSPF_config (all_devices)

    print()
    print ('Interface and OSPF configuration ERASED')
    print()

    end_time = datetime.now()
    total_time = end_time - start_time
    print ()
    print ("TOTAL_TIME with Nornir  parallelization for canceling config: {0} ".format (total_time))
    print ()

#config interfaces

    interface_config (all_devices)

#config OSPF

    ospf_config (all_devices) 

    print ()
    print ('Interface configuration DONE')
    print ()
    print ('OSPF configuration DONE')

    end_time = datetime.now()
    total_time = end_time - start_time
    print ()
    print ("TOTAL_TIME with Nornir parallelization for introducing new config: {0} ".format (total_time))
    print ()

#check configuration

    time.sleep(30)

    check_int_config (all_devices)
    show_OSPF_adj (all_devices)


if __name__ == "__main__":
    main()