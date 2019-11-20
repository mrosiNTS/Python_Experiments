import sys

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

