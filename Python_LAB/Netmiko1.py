#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import netmiko, sys
from datetime import datetime

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
for a_device in all_devices:    
    net_connect = netmiko.ConnectHandler(**a_device)
    output1 = net_connect.send_command('show cdp neighbors detail')
    output2 = net_connect.send_command('show version ') 
    print ("\n\n+++++++++++++ Device {0} ++++++++++++++++".format(a_device['device_type']))
    print (output1) 
    print (output2)
    print ("++++++++++++++ END ++++++++++++")

end_time = datetime.now()
total_time = end_time - start_time
print ()
print ("TOTAL_TIME_without_parallelization: {} ".format (total_time))
print ()
