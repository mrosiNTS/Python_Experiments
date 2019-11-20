#!/usr/bin/env python3
import sys
import getopt
from access_func import taskTOdo
from netaddr import *

def usage():

    print("Usage: {} [OPTIONS]".format(sys.argv[0]))
    print("  -m  (i.e. 10.1.2.1/30) Provide the mgmt IP address to access")
    print("  -s  (i.e. 0/3) Shutdown Interface")
    print("  -a  (i.e. 0/3-10.1.2.1/30) Assign an IP address to the Interface")
    sys.exit(1)

def main():

	# Checking options
    if len(sys.argv) == 1:
        usage()

    FLAG = None
    SHUTDOWN = False
    INTERFACE = None
    ADDRESS = None
    MASK = None

    # Reading options
    opts, args = getopt.getopt(sys.argv[1:], "m:o:s:a:")

    for opt, arg in opts:
        if opt in ['-m']:
            ADDRESS = arg[:arg.index("/")]
            IP_MASK = IPNetwork(arg)
            MASK = str(IP_MASK.netmask)   
        elif opt in ['-s']:
            SHUTDOWN = True
            INTERFACE = "interface gigabitEthernet"+arg
        elif opt in ['-a']:
            INTERFACE = "interface gigabitEthernet"+arg[:arg.index("-")]
            ADDRESS = arg[arg.find("-")+1:arg.rfind("/")]
            IP_MASK = IPNetwork(arg[arg.find("-")+1:])
            MASK = str(IP_MASK.netmask)
    
    FLAG = opt
    
    taskTOdo(FLAG, SHUTDOWN, INTERFACE, ADDRESS, MASK)

if __name__ == "__main__":
    main()
    sys.exit(0)