#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from __future__ import print_function, unicode_literals
from netmiko import ConnectHandler
from multiprocessing import Process
from datetime import datetime
import time
import xlrd
import xlwt
import re

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

def export_to_excel (Output_Interface, Output_OSPF, devices):

    int_entry = []
    OSPF_entry = []

    elements_Interface = len(Output_Interface)
    elements_OSPF = len(Output_OSPF)

    for i in range (0, elements_Interface):
        int_entry.append(Output_Interface[i].split())

    for i in range (0, elements_OSPF):
        Output_OSPF[i] = Output_OSPF[i].replace('\n', '  ')
    for i in range (0, elements_OSPF):
        OSPF_entry.append(re.split(r'\s{2,}', Output_OSPF[i]))
        OSPF_entry[i].pop(0)

    num_node = 3
    int_len = 6
    OSPF_len = 6
    int_len_total = len (int_entry[0])
    OSPF_len_total = len (OSPF_entry[0])

    data = xlwt.Workbook()
    sheet1 = data.add_sheet ("Sheet_Interfaces")
    sheet2 = data.add_sheet ("Sheet_OSPF")

    for j in range (0, int_len):
        sheet1.write (0,j, int_entry[0][j])

    x_pos = 0
    y_pos = 0

    for i in range (0,num_node):
        for j in range (int_len,int_len_total):
            y_pos = (j % int_len)
            if y_pos == 0:
                x_pos += 1
            sheet1.write (x_pos,y_pos, int_entry[i][j])

    x_pos = 0
    y_pos = 0

    for j in range (0, OSPF_len):
        sheet2.write (0,j, OSPF_entry[0][j])

    for i in range (0,num_node):
        for j in range (OSPF_len,OSPF_len_total):
            y_pos = (j % OSPF_len)
            if y_pos == 0:
                x_pos += 1
            sheet2.write (x_pos,y_pos, OSPF_entry[i][j])


    data.save ('Excel_sheet_output.xls')

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

    output = remote_conn.send_command("show ip interface brief")

    remote_conn.disconnect()

    return output

def show_OSPF_adj(a_device):

    remote_conn = ConnectHandler(**a_device)

    output = remote_conn.send_command("show ip ospf neighbor")

    remote_conn.disconnect()

    return output

############################ main #########################################

def main():

    start_time = datetime.now()
    
    processes = []
    procs = []
    a_device = []

# config cleaning (interfaces and OSPF)

    for a_device in all_devices:
        my_proc = Process(target=clean_interface_config, args=(a_device,))
        my_proc.start()
        procs.append(my_proc)
    
    for a_device in all_devices:
        my_proc = Process(target=clean_interface_config, args=(a_device,))
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

#import IP address from excel 

    IP_ADD = import_from_Excel ("adress.xlsx")

#config interfaces

    i = 0
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

    time.sleep(30)

#check configuration 

    a_device = []
    out_int_final = []
    out_OSPF_final = []

    for a_device in all_devices:
        out_int = check_int_config (a_device,)
        out_int_final.append(out_int)      
        out_OSPF = show_OSPF_adj (a_device,)
        out_OSPF_final.append(out_OSPF)

#export show's output to Excel

    export_to_excel (out_int_final, out_OSPF_final, all_devices)

if __name__ == "__main__":
    main()