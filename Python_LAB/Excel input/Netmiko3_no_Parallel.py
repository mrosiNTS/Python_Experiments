#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from __future__ import print_function, unicode_literals
from netmiko import ConnectHandler
from datetime import datetime
import time
import xlrd

from Routers_definition import all_devices

################## cleaning previous config ###########################

def import_from_Excel (Excel_sheet):

    address = xlrd.open_workbook(Excel_sheet)
    sheet = address.sheet_by_index(0)
    row = sheet.nrows
    column = sheet.ncols
    IP_ADD = []

    for k in range (1,column):
        IP_ADD.append([int(sheet.cell_value(1, k)), int(sheet.cell_value(2, k))])

    return IP_ADD

def open_multiple_SSH_session (devices):

    remote_conn = []
    a_device = []

    for a_device in devices:
        remote_conn.append(ConnectHandler(**a_device))

    return remote_conn

def clean_interface_config (remote_conn):

    intf = 0
    num_max_interfaces = 2

    for intf in range(num_max_interfaces):
        Interface_commands = ['default interface gigabitEthernet 0/{0}'.format(intf), 'exit']
        remote_conn.send_config_set(Interface_commands)

def clean_OSPF_config(remote_conn):

    Interface_commands = ['no router ospf 10', 'exit']
    remote_conn.send_config_set(Interface_commands)

################# deploying the new configuration ######################

def interface_config(remote_conn, a_device, IP_address, i):

    intf = 0
    num_max_interfaces = 2

    for intf in range(num_max_interfaces):
        Interface_commands = ['interface gigabitEthernet 0/{0}'.format(intf), 'no switchport', 'ip address 10.0.0.{0} 255.255.255.252'.format(IP_address[i][intf]), 'no shutdown', 'exit']
        remote_conn.send_config_set(Interface_commands)

def ospf_config(remote_conn, a_device):
    
    OSPF_commands = ['configure terminal', 'router ospf 10', 'router-id {0}'.format(a_device['ip']), 'network 10.0.0.0 0.0.0.15 area 0', 'exit']
    remote_conn.send_config_set(OSPF_commands)

###################### cheking configuration applied #####################

def check_int_config(remote_conn, a_device):

    print()
    print ("++++++++++++++++++++++ Router {0} +++++++++++++++++++++".format(a_device['ip']))
    print()
    print(remote_conn.send_command("show ip interface brief"))
    print()
    print ("++++++++++++++++++++++++++ END ++++++++++++++++++++++++")
    print() 

def show_OSPF_adj(remote_conn, a_device):

    print()
    print ("++++++++++++++++++++++ Router {0} +++++++++++++++++++++".format(a_device['ip']))
    print()
    print(remote_conn.send_command("show ip ospf neighbor"))
    print()
    print ("++++++++++++++++++++++++++ END ++++++++++++++++++++++++")
    print()

############################ main #########################################

def main():

    start_time = datetime.now()
    
    a_device = []
    i = 0

# open multiple SSH sessions

    remote_connection = open_multiple_SSH_session (all_devices)
    
# config cleaning (interfaces and OSPF)

    for a_device in all_devices:
        clean_interface_config (remote_connection[i],)
        i +=1

    i = 0

    for a_device in all_devices:
        clean_interface_config (remote_connection[i],)
        i +=1

    print()
    print ('Interface and OSPF configuration ERASED')
    print()

    end_time = datetime.now()
    total_time = end_time - start_time
    print ()
    print ("TOTAL_TIME without parallelization for canceling config: {0} ".format (total_time))
    print ()

#import IP address from excel 

    IP_ADD = import_from_Excel ("adress.xlsx")

#config interfaces

    i = 0
    a_device = []

    for a_device in all_devices:
        interface_config (remote_connection[i], a_device, IP_ADD, i)
        i += 1

#config OSPF

    a_device = []
    i = 0

    for a_device in all_devices: 
        ospf_config (remote_connection[i], a_device) 
        i += 1

    print ()
    print ('Interface configuration DONE')
    print ()
    print ('OSPF configuration DONE')

    end_time = datetime.now()
    total_time = end_time - start_time
    print ()
    print ("TOTAL_TIME without parallelization for introducing new config: {0} ".format (total_time))
    print ()

#check configuration
    
    a_device = []
    i = 0

    time.sleep(30)

    for a_device in all_devices:
        check_int_config (remote_connection[i], a_device)
        show_OSPF_adj (remote_connection[i], a_device)
        i +=1

if __name__ == "__main__":
    main()