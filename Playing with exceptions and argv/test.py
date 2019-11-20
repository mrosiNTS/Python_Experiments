#!/usr/bin/env python3
import sys

def sys_function():
    print (sys.version)
    print ('nome script', sys.argv[0])
    print ('number of arguments', len(sys.argv))
    print ('the arguments are', str(sys.argv))

def try_and_exception():
	a = 10
	b = 2
	try:
		print (a/b)
	except ZeroDivisionError:
			print ('division by zero')



