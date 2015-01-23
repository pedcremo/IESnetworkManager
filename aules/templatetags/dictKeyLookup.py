from django import template
from aules.models import Classroom
from aules.models import Computer
from aules.models import FirewallRule
from RosAPI import Core,Networking
from aules.MikrotikRouter import MikrotikRouter

register = template.Library()

@register.filter
def dictKeyLookup(the_dict, key):
   # Try to fetch from the dict, and if it's not found return an empty string.
   return the_dict.get(key)

#Returns True (Internet ON)  or False (Internet OFF). key parameter is a Classroom identifier

@register.filter
def is_internet_on(the_dict,key_classroom_id):
   return the_dict.get(key_classroom_id)['internet']

@register.filter
def is_internet_on_pc(computer,mac):

	
	network_type=computer.classroom.network_device.network_type 
    
  	if network_type=="Mikrotik":  	
		
			mk =MikrotikRouter()
			mk.set_networkdevice(computer.classroom.network_device)
			#mk.login()
			resposta = mk.list_firewall_rule_by_mac(mac)
			#print "DEBUG -->"+resposta
			if resposta: 
				return False
			else:
				return True
		
	else:
		return True
