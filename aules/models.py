from django.db import models
from MacModel import MACAddressField

# Create your models here.
# Author Pere Crespo Molina

NETMASK = (
		(32,u'32 bits'),
		(24,u'24 bits'),
		(16,u'16 bits'),
		(8,u'8 bits'),
		(0,u'0 bits'),
	)

class UrlListItem(models.Model):
	
	comment = models.CharField(u'Comentari',max_length=255,blank=True,null=True)
	url = models.URLField('URL',max_length=200,blank=True, null=True)
	#generic_ip = models.GenericIPAddressField(blank=True, null=True, unique=True)
	ip_address = models.GenericIPAddressField(blank=True, null=True)
	netmask = models.IntegerField('Mascara xarxa',choices=NETMASK,default=32)
	
	
	def __unicode__(self):
		return unicode(self.comment)


class UrlList(models.Model):
	url_list_items = models.ManyToManyField(UrlListItem)
	name = models.CharField(max_length=150)
	comment = models.CharField(max_length=255,blank=True,null=True)
	
	def __unicode__(self):
		return unicode(self.name)
		

#Includes switches and routers with a programatic API in order to manage it
#Currently we only have Mikrotik devices with their propietary API but It would
#be nice to code something for Open vSwitch compatible devices http://openvswitch.org/
class ApiNetworkDevice(models.Model):

	TYPES = (
		("Mikrotik",u'Dispositius Mikrotik amb API activada i sistema RouterOS'),
		("Iptables",u'Sistema Linux amb ssh activat i Iptables'),
		("Openvswitch",u"Sistema estàndar openvswitch suportat per molts fabricants de xarxes com (cisco, juniper ...)"),
    )
	name = models.CharField(u'Nom dispositiu',max_length=150)
	comment = models.CharField(u'Comentari',max_length=255,blank=True,null=True)
	ip = models.IPAddressField(u'Adreça IP')
	admin =models.CharField('Login admin',max_length=50)	
	password = models.CharField('Password',max_length=50)
	network_type = models.CharField(u'Tipus dispositiu',choices=TYPES,max_length=150,help_text="Actualment solament soportem API de Mikrotik amb routeros")
	
	def __unicode__(self):
		return self.name
		
class FirewallRule(models.Model):
	ACTIONS = (
		("DROP",u'DROP Si activada aleshores deneguem pas dels paquets de xarxa'),
		("ACCEPT",u'ACCEPT Si activada aleshores acceptem pas dels paquets de xarxa'),
		("REDIRECT",u'REDIRECT Si activada aleshores redireccionem els paquets a una URL'),
	)

	network_device = models.ForeignKey(ApiNetworkDevice,verbose_name='Dispositiu de xarxa',help_text="Aquest dispositiu amb API aplicarà de manera efectiva la regla del firewall (<a href='http://mikrotik.com/'>Mikrotik</a>, iptables linux PC, <a href='http://openvswitch.org/'>openvswitch</a>  ...)")	
	dst_ip_list = models.ForeignKey(UrlList,verbose_name='Llistat IPs',help_text="Llistat IPs de destí a les que s'aplica la regla. MOLT IMPORTANT")
	comment = models.CharField(u'Nom de la regla',help_text="És important un nom descriptiu del que fa la regla. Aquest nom és el que apareixerà quan seleccionem la regla per a un aula",max_length=255)
	action = models.CharField(u'Acció',max_length=100,choices=ACTIONS)
	redirect_url = models.URLField(verbose_name="URL de redirecció",help_text="S'aplica solament si ACTION = REDIRECT ",blank=True)
	src_address=models.GenericIPAddressField(verbose_name=u"Adreça IP font(src)",help_text="Pot ser també una adreça de xarxa.És opcional perquè tal vegada preferim filtrar per Llistat IPs o Adreça IP destí",blank=True, null=True)
	src_netmask = models.IntegerField('Mascara xarxa src',choices=NETMASK,help_text="24 bits = 255.255.255.0, 16 bits = 255.255.0.0  ...",default=32,blank=True)

	#dst_address=models.GenericIPAddressField(verbose_name=u"Adreça IP destí(dst)",help_text="Pot ser també una adreça de xarxa.És opcional perquè tal vegada preferim filtrar per Llistat IPs o Adreça IP font",blank=True, null=True)
	#dst_netmask = models.IntegerField('Mascara xarxa dst',choices=NETMASK,help_text="24 bits = 255.255.255.0, 16 bits = 255.255.0.0  ...",default=32,blank=True)
	
	src_mac_address=MACAddressField(u'Source MAC address',help_text="Aquesta opció és per quan volem filtrar un PC per MAC",blank=True,null=True)
	
	is_active = models.BooleanField(u'ACTIVADA',default=False)
	
	def __unicode__(self):
		return unicode(self.comment)
	
class Classroom(models.Model):
	name = models.CharField(u'Aula',max_length=150)
	comment = models.CharField(u'Comentari',max_length=255,blank=True,null=True)
	firewall_rule= models.ForeignKey(FirewallRule,verbose_name=u"Regla de Firewall Aula", help_text=u"Si no tenim regla de firewall per a l'aula activarem opció de baix(Filtrar Aula per MAC)",blank=True,null=True)
	mac_filter = models.BooleanField(verbose_name=u"Filtrar Aula per MAC",help_text="Filtrarem l'accés a Internet de l'aula utilitzant cada una de les MACs dels PCs que la composen",default=False)
	network_device = models.ForeignKey(ApiNetworkDevice,verbose_name='Dispositiu de xarxa',help_text="Aquest dispositiu amb API aplicarà de manera efectiva la regla del firewall (<a href='http://mikrotik.com/'>Mikrotik</a>, iptables linux PC, <a href='http://openvswitch.org/'>openvswitch</a>  ...)")	

	def __unicode__(self):
		return self.name



class PCmodel(models.Model):
	ARCHITECTURE_CHOICES = (
		(32,u'32 bits'),
		(64,u'64 bits'),
	)
	VIRTUALIZATION_CHOICES = (
		(0,u'No'),
		(1,u'Si'),
	)	
	motherboard = models.CharField('Model Placa base',max_length=150)
	ram = models.IntegerField('RAM en GB')
	hdd = models.IntegerField('Disc Dur en GB')
	cpu = models.CharField('Tipus de CPU',max_length=100)
	architecture = models.IntegerField('Arquitectura',choices=ARCHITECTURE_CHOICES)
	cpu_virtualization = models.IntegerField('Virtualització?',choices=VIRTUALIZATION_CHOICES)
	comment = models.CharField('Comentari',max_length=255,blank=True,null=True)	
		
	def __unicode__(self):
		return self.cpu + " " +str(self.architecture)+"bits "+self.motherboard
	
	
		

	
class Computer(models.Model):
	classroom = models.ForeignKey(Classroom,verbose_name="Aula")
	model = models.ForeignKey(PCmodel)
	#firewall_rule= models.ForeignKey(FirewallRule)
	#controller_apinetworkdevice = models.ForeignKey(ApiNetworkDevice)
	identifier = models.CharField('Id PC',max_length=100)
	#mac = models.CharField(max_length=18)
	mac = MACAddressField('MAC address')
	comment = models.CharField('Comentari',max_length=255,blank=True,null=True)
	buying_date = models.DateField('Data alta',blank=True,null=True)
	serial = models.CharField(u'Núm. sèrie',max_length=50)
	is_active = models.BooleanField(u'Està en servei?',default=True)
	
	def is_blocked(self):
		return True;
	def __unicode__(self):
		return self.identifier +" "+ unicode(self.classroom)


	
	
