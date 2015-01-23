import sys
import socket 
import re
from datetime import datetime
import logging 

from django.utils.timezone import now,utc
    

#This is the way to use a django model from an external application
#http://www.b-list.org/weblog/2007/sep/22/standalone-django-scripts/
from django.core.management import setup_environ
from manager import settings
setup_environ(settings)
from proxylog.models import ProxyEntry

#Use logger for ERRORS
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('ERROR_udp_server.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

#Server newtwork conf
UDP_IP = "192.168.5.10"
UDP_PORT = 514
sock = socket.socket(socket.AF_INET, # Internet
			socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

print "Servidor UDP escoltant en port "+str(UDP_PORT)+" i IP "+UDP_IP
print "\n Esperant que un proxy envie informació de navegació"
	
while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	m = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', data)
	ip = m.group(0)	
	m=re.search('(htt(p|ps):\/\/[a-z0-9.-]*)',data)
	url = m.group(0)
	#print "received message:", data
	now = datetime.utcnow().replace(tzinfo=utc)	
	#now = datetime.now()
	pe = ProxyEntry(event_date=now,ip_src=ip,domain_destination=url)
	try:
		pe.save()
	except:
		logger.error('DATABASE ERROR: %s', sys.exc_info()[0])
	else:
		if ip.startswith('192.168'):
			print "Entrada: ", ip+" "+url
			#logger.error('Entrada: %s %s',ip,url)
	#print "Altra Entrada:", ip +" "+url
