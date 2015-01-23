from aules.models import FirewallRule
from aules.models import ApiNetworkDevice
from RosAPI import Core,Networking
import socket
from django.conf import settings

## Singleton class

class MikrotikRouter(Exception):

	debug = True
	## Stores the unique Singleton instance
   	_iInstance = None

	#def __init__(self,networkdevice):
	#	print "DEBUG --> POOO" 
	#	self.net_device=networkdevice
	
	## Class used with this Python singleton design pattern
    	#  @todo Add all variables, and methods needed for the Singleton class below
    	class Singleton:
        	def __init__(self):
            		## specific Mikrotik network device
            		self.net_device = None
			## Stablished connection?
			self.tik = None
	## The constructor
    	#  @param self The object pointer.
    	def __init__( self ):
		# Check whether we already have an instance
		self.net_device = None
        	"""if MikrotikRouter._iInstance is None:
            		# Create and remember instanc
            		MikrotikRouter._iInstance = MikrotikRouter.Singleton()
		# Store instance reference as the only member in the handle
        	self._EventHandler_instance = MikrotikRouter._iInstance"""

	def set_networkdevice(self, networkdevice_):

		self.net_device = networkdevice_
		"""if self.net_device is None:
			self.net_device = networkdevice_
			self.tik = None
		else:
			if self.net_device.id !=  networkdevice_.id:
				self.tik = None
				self.net_device = networkdevice_	
		"""
	
	## Delegate access to implementation.
    	#  @param self The object pointer.
    	#  @param attr Attribute wanted.
    	#  @return Attribute
    	#def __getattr__(self, aAttr):
        #	return getattr(self._iInstance, aAttr)
 
 
    	## Delegate access to implementation.
    	#  @param self The object pointer.
    	#  @param attr Attribute wanted.
    	#  @param value Vaule to be set.
    	#  @return Result of operation.
    	#def __setattr__(self, aAttr, aValue):
        #	return setattr(self._iInstance, aAttr, aValue)	
	
	def login(self):
		try:
			
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print "DEBUG --> LOGIN2 "+ self.net_device.ip
			s.connect((self.net_device.ip, 8728))
			
			self.tik = Core(s, DEBUG=self.debug)
			
			self.tik.login(username=self.net_device.admin, pwd=self.net_device.password)
		except Exception, e:	
			raise RuntimeError("No puc connectar amb el router")
			#raise MikrotikRouter, ("No puc connectar amb el router", e)
			
	def add_firewall_rule(self,comment,src_address,src_netmask,dst_address_list=None,action="drop"):
		try:
			#if not self.tik or self.tik is None:
			self.login()			
			id_rule=self.get_id_first_rule()
			''' Volem posar la regla a la primera posició del firewall'''
			if id_rule is None:
				if dst_address_list is None:
					print "pesjslsld 1 "+action
					print "pesjslsld 1 "+comment
					print "pesjslsld 1 "+src_address
					print "pesjslsld 1 "+src_netmask
					
					word = ["/ip/firewall/filter/add","=chain=forward","=action="+action,"=comment="+comment,"=src-address="+src_address+"/"+src_netmask]
				else:
					word = ["/ip/firewall/filter/add","=chain=forward","=action="+action,"=comment="+comment,"=dst-address-list="+dst_address_list]
			else:
				print "pesjslsld"
				
				if dst_address_list is None:
					print "pesjslsld 2 "+action
					print "pesjslsld 2 "+comment
					print "pesjslsld 2 "+src_address
					print "pesjslsld 2 "+src_netmask
					word = ["/ip/firewall/filter/add","=chain=forward","=action="+action,"=comment="+comment,"=src-address="+src_address+"/"+src_netmask,"=place-before="+id_rule]
					print word
				else:
					print "pesjslsld 1"
					word = ["/ip/firewall/filter/add","=chain=forward","=action="+action,"=comment="+comment,"=dst-address-list="+dst_address_list,"=place-before="+id_rule]
					print "pesjslsld 122111"
					print word
			
			if self.debug:
				print word
			resposta = self.tik.talk( word)
			resposta = self.tik.response_handler(resposta)
			
			if self.debug:
				print resposta
		
		except Exception, e:
				raise MikrotikRouter, ("No puc aplicar regla de firewall",e )
	
	def add_firewall_rule_by_mac(self,mac,action="drop"):
		try:
			mac=mac.upper()
			#if not self.tik or self.tik is None:
			self.login()			
			id_rule=self.get_id_first_rule()
			''' Volem posar la regla a la primera posició del firewall'''			
			if id_rule is None:
				word = ["/ip/firewall/filter/add","=chain=forward","=action="+action,"=comment="+mac,"=src-mac-address="+mac]
			else:
				word = ["/ip/firewall/filter/add","=chain=forward","=action="+action,"=comment="+mac,"=src-mac-address="+mac,"=place-before="+id_rule]
			resposta = self.tik.talk( word)
			resposta = self.tik.response_handler(resposta)
			
			if self.debug:
				print resposta
		
		except Exception, e:
				raise MikrotikRouter, ("No puc aplicar regla de firewall per MAC",e )
	
	''' vull que siga privada TODO '''
	def get_id_first_rule(self):
			word = ["/ip/firewall/filter/print"]
			resposta = self.tik.talk( word)
			resposta = self.tik.response_handler(resposta)
			if resposta:
				first_item=resposta[0]
				return first_item['.id']
			else:
				return None

	def delete_firewall_rule_by_mac(self,mac,action="drop"):
		try:
			mac=mac.upper()
			#if not self.tik or self.tik is None:
			self.login()
			word = ["/ip/firewall/filter/print","?comment="+mac,"?src-mac-address="+mac,"?action="+action]
			resposta = self.tik.talk( word)
			resposta = self.tik.response_handler(resposta)
			
			if self.debug:
				print resposta
			
			for item in resposta:
				word = ["/ip/firewall/filter/remove","=.id="+item['.id']]
				resposta = self.tik.talk( word)
				resposta = self.tik.response_handler(resposta)
				if self.debug:
					print resposta
		except Exception, e:
			raise MikrotikRouter, ("No puc esborrar regla de firewall",e )
			
	def list_firewall_rule(self,comment,src_address=None,src_netmask=None):
		try:
			
			#if (not self.tik) or (self.tik is None):
			self.login()
			if src_address is None:
				word = ["/ip/firewall/filter/print","?comment="+comment]
			else:
				word = ["/ip/firewall/filter/print","?comment="+comment,"?src-address="+src_address+"/"+src_netmask]
				
			resposta = self.tik.talk( word)
			resposta = self.tik.response_handler(resposta)
			
			if self.debug:
				print resposta
			return resposta
		except Exception, e:
			raise MikrotikRouter, ("No puc llistar regla de firewall",e )
	
	def list_firewall_rule_by_mac(self,mac,action=None):
		try:
			mac=mac.upper()
			#print "DEBUG -->"+mac+" Xxx" 
			if not self.tik or self.tik is None:
				self.login()
			if action is None:
				word = ["/ip/firewall/filter/print","?comment="+mac,"?src-mac-address="+mac]
			else:			
				word = ["/ip/firewall/filter/print","?comment="+mac,"?src-mac-address="+mac,"?action="+action]
			resposta = self.tik.talk( word)
			resposta = self.tik.response_handler(resposta)
			print "DEBUG --> Xxxxx" 
			if self.debug:
				print resposta
			return resposta
		except Exception, e:
			raise MikrotikRouter, ("No puc llistar regla de firewall",e )
			
	def delete_firewall_rule(self,comment):
		try:
			#if not self.tik or self.tik is None:
			self.login()			
			word = ["/ip/firewall/filter/print","?comment="+comment]
			resposta = self.tik.talk( word)
			resposta = self.tik.response_handler(resposta)
			
			if self.debug:
				print resposta
			
			for item in resposta:
				word = ["/ip/firewall/filter/remove","=.id="+item['.id']]
				resposta = self.tik.talk( word)
				resposta = self.tik.response_handler(resposta)
				if self.debug:
					print resposta
		except Exception, e:
			raise MikrotikRouter, ("No puc esborrar regla de firewall",e )
			
	''' HARD WIRED enable or disable Nat Firewall rule based on their comment '''
	''' Regla utilitzada per habilitar amb pinces algunes regles de src nat per permetre barra lliure '''	

	def enable_disable_firewall_nat_rule(self,comment_rule,on_off):
		try:
			
			self.login()		
			#print "2PPPPP "+id_rule+" ON_OFF="+on_off 
			word = ["/ip/firewall/nat/print","?comment="+comment_rule]
			resposta = self.tik.talk( word)
			resposta = self.tik.response_handler(resposta)
			
			for item in resposta:				
				if on_off == "0":
					word = ["/ip/firewall/nat/disable","=.id="+item['.id']]
				else:
					word = ["/ip/firewall/nat/enable","=.id="+item['.id']]
				resposta = self.tik.talk( word)
				resposta = self.tik.response_handler(resposta)
				if self.debug:
					print resposta
			
			if self.debug:
				print resposta
			
		except Exception, e:
			raise MikrotikRouter, ("No puc habilitar/deshabilitar regla de firewall nat",e )

	''' HARD WIRED check if a Nat Firewall rule is enabled or disabled based on their comment '''	
	def is_firewall_nat_rule_enabled(self,comment_rule):
		#try:
			
			self.login()		
			#print "2PPPPP "+id_rule+" ON_OFF="+on_off 
			word = ["/ip/firewall/nat/print","?comment="+comment_rule,"?disabled=true"]
			resposta = self.tik.talk( word)
			resposta = self.tik.response_handler(resposta)

			if self.debug:
				print resposta

			# Si no hi ha resposta, aquesta regla de NAT esta deshabilitada 
			if not resposta :
				return True
			# Si hi ha resposta, aquesta regla de NAT esta habilitada 
			else:
				return False	

		 #Exception, e:
		 #	raise MikrotikRouter, ("No puc habilitar/deshabilitar regla de firewall nat",e )

		
	def delete_classroom_firewall_rules(self,classroom):
		
		computers=classroom.computer_set.all()
		
		try:
			self.login()
			
			for pc in computers:		
				
				word = ["/ip/firewall/filter/print","?src-mac-address="+pc.mac.upper()]
				resposta = self.tik.talk( word)
				resposta = self.tik.response_handler(resposta)
				for item in resposta:
					word = ["/ip/firewall/filter/remove","=.id="+item['.id']]
					resposta = self.tik.talk( word)
					resposta = self.tik.response_handler(resposta)
		except Exception, e:
			raise MikrotikRouter, ("No puc esborrar regla de firewall",e )
	
	''' Add list of IP addresses to the firewall '''
	def add_firewall_list(self,url_list_items,list_id):
		try:
			
			self.login()		
			self.list_remove(list_id)
			for item in url_list_items: 
				#if not self.list_item_exist(str(item.ip_address),str(item.netmask),list_id):						  		
					word = ["/ip/firewall/address-list/add","=address="+str(item.ip_address)+'/'+str(item.netmask),"=list="+list_id]
					resposta = self.tik.talk(word)
					resposta = self.tik.response_handler(resposta)
			if self.debug:
				print resposta	
		except Exception, e:
			raise MikrotikRouter, ("No puc afegir llista al firewall",e )
	
	''' Remove list '''
	def list_remove(self,list_id):
		try:
			word = ["/ip/firewall/address-list/print","?list="+list_id]
			resposta = self.tik.talk(word)
			resposta = self.tik.response_handler(resposta)

			for item in resposta:
					word = ["/ip/firewall/address-list/remove","=.id="+item['.id']]
					resposta = self.tik.talk( word)
					resposta = self.tik.response_handler(resposta)
					
			if self.debug:
				print resposta	
		except Exception, e:
			raise MikrotikRouter, ("No puc esborrar item llista del firewall",e )
	
	''' Check if list item exists '''
	def list_item_exist(self,ip_address,netmask,list_id):
		try:
			#This is a fix, router os eliminate/hide 32 masks
			if netmask!="32":
				ip_address=ip_address+"/"+netmask
			word = ["/ip/firewall/address-list/print","?address="+ip_address,"?list="+list_id]
			resposta = self.tik.talk(word)
			resposta = self.tik.response_handler(resposta)

			if resposta:				
				return True
			else:
				return False

			if self.debug:
				print resposta	
		except Exception, e:
			raise MikrotikRouter, ("No puc consultar item llista del firewall",e )
	
	def block_classroom_by_mac(self,classroom,comment=None,action="drop"):
		try:
			classroom_pcs=classroom.computer_set.all().order_by('identifier')
			self.login()			

			for pc in classroom_pcs:
				mac=pc.mac.upper()
				#if not self.tik or self.tik is None:
			
				id_rule=self.get_id_first_rule()
				if comment is None:
					comment=settings.FW_PREFIX+' '+mac				
				
				''' Volem posar la regla a la primera posició del firewall'''			
				if id_rule is None:
					word = ["/ip/firewall/filter/add","=chain=forward","=action="+action,"=comment="+comment,"=src-mac-address="+mac]
				else:
					word = ["/ip/firewall/filter/add","=chain=forward","=action="+action,"=comment="+comment,"=src-mac-address="+mac,"=place-before="+id_rule]
				resposta = self.tik.talk( word)
				resposta = self.tik.response_handler(resposta)
			
				if self.debug:
					print resposta
		
		except Exception, e:
				raise MikrotikRouter, ("No puc aplicar regla de firewall per MAC",e )


	
