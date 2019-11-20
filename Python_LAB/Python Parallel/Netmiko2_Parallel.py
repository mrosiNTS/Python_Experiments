#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from __future__ import print_function, unicode_literals
import sys
from netmiko import ConnectHandler
from multiprocessing import Process
from datetime import datetime
import time

from INTERFACEs_Def import IP_ADD

################## cleaning previous config ###########################

def clean_interface_config(a_device):

    intf = 0
    num_max_interfaces = 2

    remote_conn = ConnectHandler(**a_device)

    for intf in range(num_max_interfaces):
        Interface_commands = ['default interface gigabitEthernet 0/{0}'.format(intf), 'exit']
        remote_conn.send_config_set(Interface_commands)

    remote_conn.disconnect()


def clean_OSPF_config(a_device):

    remote_conn = ConnectHandler(**a_device)

    Interface_commands = ['no router ospf 10', 'exit']
    remote_conn.send_config_set(Interface_commands)

    remote_conn.disconnect()

################# deploying the new configuration ######################

def interface_config(a_device, IP_address, i):

    intf = 0
    num_max_interfaces = 2

    remote_conn = ConnectHandler(**a_device)

    for intf in range(num_max_interfaces):
        Interface_commands = ['interface gigabitEthernet 0/{0}'.format(intf), 'no switchport', 'ip address 10.0.0.{0} 255.255.255.252'.format(IP_address[i][intf]), 'no shutdown', 'exit']
        remote_conn.send_config_set(Interface_commands)

    remote_conn.disconnect()

def ospf_config(a_device):
    
    OSPF_commands = ['configure terminal', 'router ospf 10', 'router-id {0}'.format(a_device['ip']), 'network 10.0.0.0 0.0.0.15 area 0', 'exit']
    
    remote_conn = ConnectHandler(**a_device)
    
    remote_conn.send_config_set(OSPF_commands)

    remote_conn.disconnect()

###################### cheking configuration applied #####################

def check_int_config(a_device):

    remote_conn = ConnectHandler(**a_device)

    print()
    print ("++++++++++++++++++++++ Router {0} +++++++++++++++++++++".format(a_device['ip']))
    print()
    print(remote_conn.send_command("show ip interface brief"))
    print()
    print ("++++++++++++++++++++++++++ END ++++++++++++++++++++++++")
    print() 

    remote_conn.disconnect()

def show_OSPF_adj(a_device):

    remote_conn = ConnectHandler(**a_device)

    print()
    print ("++++++++++++++++++++++ Router {0} +++++++++++++++++++++".format(a_device['ip']))
    print()
    print(remote_conn.send_command("show ip ospf neighbor"))
    print()
    print ("++++++++++++++++++++++++++ END ++++++++++++++++++++++++")
    print()

    remote_conn.disconnect()

############################ main #########################################

def main():
    router1 = {
        'device_type': 'cisco_ios',
        'ip': sys.argv[1],
        'username': 'cisco',
        'password': 'cisco',
        'port': 22,
        'verbose': False 
    }
    router2 = {
        'device_type': 'cisco_ios',
        'ip': sys.argv[2],
        'username': 'cisco',
        'password': 'cisco',
        'port': 22,
        'verbose': False 
    }
    router3 = {
        'device_type': 'cisco_ios',
        'ip': sys.argv[3],
        'username': 'cisco',
        'password': 'cisco',
        'port': 22,
        'verbose': False 
    }

    all_devices = [router1, router2, router3]
    start_time = datetime.now()
    
    i = 0
    processes = []
    procs = []
    a_device = []

# pulizia config

    for a_device in all_devices:
        my_proc = Process(target=clean_interface_config, args=(a_device,))
        my_proc.start()
        procs.append(my_proc)

    for a_device in all_devices:
        my_proc = Process(target=clean_OSPF_config, args=(a_device,))
        my_proc.start()
        procs.append(my_proc)

    for processes in procs:
        processes.join()

    print()
    print ('Interface and OSPF configuration ERASED')
    print()

    end_time = datetime.now()
    total_time = end_time - start_time
    print ()
    print ("TOTAL_TIME with parallelization for canceling config: {0} ".format (total_time))
    print ()

#config interfaces
    
    procs = []
    a_device = []
    processes = []

    for a_device in all_devices:
        my_proc = Process(target=interface_config, args=(a_device, IP_ADD, i))
        my_proc.start()
        procs.append(my_proc)
        i += 1

#config OSPF

    a_device = []
    processes = []

    for a_device in all_devices: 
        my_proc = Process(target=ospf_config, args=(a_device,)) 
        my_proc.start()
        procs.append(my_proc)

    for processes in procs:
        processes.join()

    print ()
    print ('Interface configuration DONE')
    print ()
    print ('OSPF configuration DONE')

    end_time = datetime.now()
    total_time = end_time - start_time
    print ()
    print ("TOTAL_TIME with parallelization for introducing new config: {0} ".format (total_time))
    print ()

#check configuration
    
    a_device = []

    time.sleep(30)

    for a_device in all_devices:
        check_int_config (a_device)

    for a_device in all_devices:
        show_OSPF_adj (a_device)


if __name__ == "__main__":
    main()