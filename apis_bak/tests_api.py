#!/usr/bin/env python

from RosAPI import Core

def prettify(data):
	for x in data:
		print "______________________________________________________________"
		for y in x.keys():
			print "%-20s: %50s" % (y, x[y])

if __name__ == '__main__':
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("10.34.240.66", 8728))
	tik = Core(s, DEBUG=False)
	tik.login(username="admin", pwd="-x@rx@3W")
	
	#a = Core('10.34.240.66:8728')
	#a.login('admin', '-x@rx@3W')
	#a.run_interpreter()
	prettify(tik.response_handler(tik.talk(['/ip/dhcp-server/lease/print'])))
