# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from aules.models import Classroom
from aules.models import Computer
from aules.models import UrlList
from aules.models import FirewallRule
from django.template import RequestContext
from django.contrib.auth import authenticate, login,logout
#from django.views.generic.simple import direct_to_template
from django.views.generic.base import TemplateView
from RosAPI import Core,Networking
from MikrotikRouter import MikrotikRouter
from pprint import pprint
from django.conf import settings
import datetime
import socket

def is_internet_on_classroom(classroom):
	print 'asasas 1.1'
	network_type=classroom.network_device.network_type
	print 'asasas 1.2'
	firewall_rule=classroom.firewall_rule
	classroom_pcs=classroom.computer_set.all().order_by('identifier')
	#First Classroom computer
	pc1=None
	if classroom_pcs:
		pc1=classroom_pcs[0]
		

	if network_type=="Mikrotik":  	
		#try:  				
			mk =MikrotikRouter()			
			mk.set_networkdevice(classroom.network_device)
			print 'asasas 1.3'
			#If we block the classroom only taking into account MAC addresses
			if classroom.mac_filter:
				
				if pc1:
					resposta = mk.list_firewall_rule(settings.FW_PREFIX+' '+pc1.mac.upper())
			else:
				print 'asasas 1.4 '+firewall_rule.comment
				resposta = mk.list_firewall_rule(firewall_rule.comment,firewall_rule.src_address,str(firewall_rule.src_netmask))
				print 'asasas 1.5'
			if resposta: 
				return False
			else:
				return True
		#except Exception ,msg:  			
  		#	return False
	else:
		return True
		
def is_internet_partial_on_classroom(classroom):

	network_type=classroom.network_device.network_type
	firewall_rule=classroom.firewall_rule
	
	if network_type=="Mikrotik":
		mk =MikrotikRouter()			
		mk.set_networkdevice(classroom.network_device)
		resposta = mk.list_firewall_rule("LLISTA-"+str(classroom.id))
		
		if resposta: 
			return resposta[0]['dst-address-list']				
		else:
			return None		
	else:
		return None

''' Retorna True si no hi ha cap regla de firewall drop basat en MAC del PC '''
'''def is_internet_on_pc(computer,mac):

	network_type=computer.classroom.network_device.network_type 
    	
  	if network_type=="Mikrotik":  	
		
			mk =MikrotikRouter()
			mk.set_networkdevice(computer.classroom.network_device)
			mk.login()
			# Si tenim internet a classe no cal regles especifiques accept per mac al firewall 
			#try:
			#	mk.delete_firewall_rule_by_mac(mac,"accept")
			#except Exception, e:
			#	pass
			
			resposta = mk.list_firewall_rule_by_mac(mac)
			
			#print "DEBUG -->"+resposta
			if resposta: 
				return False
			else:
				return True
		
	else:
		return True
	
'''	
def get_pcs_information(classroom,list_pcs_classroom):
	pcs=[]	
	network_type=classroom.network_device.network_type 
	if network_type=="Mikrotik":  			
			mk =MikrotikRouter()
			mk.set_networkdevice(classroom.network_device)
			mk.login()
			
			#print classroom
			for computer in list_pcs_classroom:
				print computer
				resposta = mk.list_firewall_rule_by_mac(computer.mac)
				if resposta:
					network_action=resposta[0]['action']
					blocked = True
				else:
					network_action=None
					blocked = False
				pcs.append({'id':computer.id,'network_action':network_action,'identifier':computer.identifier,'mac':computer.mac,'resposta':resposta,'serial':computer.serial})
	return pcs


  
def index(request):
	classroom_list = Classroom.objects.all()
	output={}
	for classroom in classroom_list:
		output[classroom.id]={'name':classroom.name}
	return render_to_response('aules/index.html', {'classroom_list': output},context_instance=RequestContext(request))
	
	
def mylogin(request):

  if request.method == 'POST':
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
      if user.is_active:
        login(request, user)
        # success
	#return direct_to_template(request, 'aules/index.html')
        return HttpResponseRedirect('/')
      else:
        # disabled account
        #return direct_to_template(request, 'aules/inactive_account.html')
        return TemplateView.as_view(template_name='aules/inactive_account.html')
    else:
      # invalid login
      #return direct_to_template(request, 'aules/invalid_login.html')
	return TemplateView.as_view(template_name='aules/invalid_login.html')
      
def mylogout(request):
  logout(request)
  return redirect('home')

def block_by_mac(request,pc_id,pc_state):
  if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
  response = HttpResponse()
  pc=Computer.objects.get(id=pc_id)
  network_type=pc.classroom.network_device.network_type 
  if network_type=="Mikrotik":    
    try:
    	mk =MikrotikRouter()
    	mk.set_networkdevice(pc.classroom.network_device)
    	mk.login()
    	
    	if pc_state == "OFF":
    		mk.add_firewall_rule_by_mac(pc.mac)    		
    	else:
    		mk.delete_firewall_rule_by_mac(pc.mac)
    	response.write("");
    except Exception, e:
    	response.write("ERROR: "+str(e))
	
  return response

def allow_by_mac(request,pc_id,pc_state):
  if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
  response = HttpResponse()
  pc=Computer.objects.get(id=pc_id)
  network_type=pc.classroom.network_device.network_type 
  if network_type=="Mikrotik":    
    try:
    	mk =MikrotikRouter()
	mk.set_networkdevice(pc.classroom.network_device)
    	mk.login()
    	
    	if pc_state == "ON":
    		mk.add_firewall_rule_by_mac(pc.mac,"accept")    		
    	else:
    		mk.delete_firewall_rule_by_mac(pc.mac,"accept")
    	response.write("");
    except Exception, e:
    	response.write("ERROR: "+str(e))
	
  return response
  
def drawing_classroom(request,classroom_id,internet_id):

  response = HttpResponse()
  classroom=Classroom.objects.get(id=classroom_id)
  error_layer=''
  response.write('<div id="aula-'+classroom_id+'" >')
  internet_in_classroom=True;
  partial_list=None
  
  try:
	print 'asasas 1'+classroom_id
        

  	if is_internet_on_classroom(classroom):
  		response.write('<h1><button class="internet ui-button" id="aula-'+classroom_id+'"></button> INTERNET &nbsp;&nbsp;&nbsp;</h1>')
  		
  		visible_partial_internet=True
		
  		partial_list=is_internet_partial_on_classroom(classroom)
		''' HARDWIRED '''	
		if classroom_id == "3":
			if is_barra_lliure_set("3"):
				response.write('<input checked="checked" id="barra-aula-'+classroom_id+'" type="checkbox" onclick="javascript:barra_lliure(\'aula-'+classroom_id+'\');" >Barra lliure</input>')
			else:
				response.write('<input id="barra-aula-'+classroom_id+'" type="checkbox" onclick="javascript:barra_lliure(\'aula-'+classroom_id+'\');" >Barra lliure</input>')
  	else:  		
  		internet_in_classroom=False
  		visible_partial_internet=False
  		response.write('<h1><button class="internet ui-button-off" id="aula-'+classroom_id+'"></button> INTERNET </h1>')
  	print 'asasas 2'
	if request.user.is_authenticated():
		response.write('<h2><a href="proxylog/aula-'+classroom_id+'" target="_blank">TOP 30</a></h2>');	

  	if visible_partial_internet:
  		if partial_list is None:
  			response.write('<h3 id="partial-aula-'+classroom_id+'"><input id="aula-'+classroom_id+'" type="checkbox" onclick="javascript:restrict(\'aula-'+classroom_id+'\');" >Restringit a:</input>')
  			response.write('<SELECT id="aula-'+classroom_id+'" style="visibility:hidden;" NAME="restrict_internet"  onChange="javascript:apply_restriction(\'aula-'+classroom_id+'\');">')
  		else:
  			response.write('<h3 id="partial-aula-'+classroom_id+'"><input id="aula-'+classroom_id+'" type="checkbox" checked="checked" onclick="javascript:restrict(\'aula-'+classroom_id+'\');" >Restringit a:</input>')
  			response.write('<SELECT id="aula-'+classroom_id+'" style="visibility:visible;" NAME="restrict_internet"  onChange="javascript:apply_restriction(\'aula-'+classroom_id+'\');">')
  	else:
  		response.write('<h3 id="partial-aula-'+classroom_id+'"><input id="aula-'+classroom_id+'" style="visibility:hidden;" type="checkbox" onclick="javascript:restrict(\'aula-'+classroom_id+'\');" >Restringit a:</input>')
  		response.write('<SELECT id="aula-'+classroom_id+'" style="visibility:hidden;" NAME="restrict_internet"  onChange="javascript:apply_restriction(\'aula-'+classroom_id+'\');">')
  		
  	#response.write('<SELECT id="aula-'+classroom_id+'" style="visibility:hidden;" NAME="restrict_internet"  onChange="javascript:apply_restriction(\'aula-'+classroom_id+'\');">')
  	url_list = UrlList.objects.all()
  	restricted_list={}
  		
  	for item_url_list in url_list:
  		#print item_url_list
  		if item_url_list.name==partial_list:
  			response.write('<OPTION  selected="selected" VALUE="'+str(item_url_list.id)+'">'+item_url_list.name+'</OPTION>')
  		else:
  			response.write('<OPTION  VALUE="'+str(item_url_list.id)+'">'+item_url_list.name+'</OPTION>')
  			
	response.write('</SELECT>') 
	response.write('</h3>')
	
  except Exception, msg:  			
  	error_layer="ERROR: "+str(msg)
  
  
  if not error_layer:
  	classroom_pcs=classroom.computer_set.all().order_by('identifier')
	try:
		pcs_inf=get_pcs_information(classroom,classroom_pcs)
  	
  		for computer in pcs_inf:
  			#response.write(computer)
  			if computer['network_action']==None:
  				if internet_in_classroom:
  					response.write('<div id="computer-'+str(computer['id'])+'" class="ui-pc-on"> ')
  					response.write('<a href="http://192.168.5.10/incidencias/frmnewext.php?login=pedcremo&idaula='+classroom_id+'&equipo='+str(computer['identifier'])+'&serial='+str(computer['serial'])+'"><img src="images/pc_mini.png"/></a>')
					response.write('<div class="desc"><button class="blockPC ui-button-pc-lock" aula="aula-'+classroom_id+'" id="'+str(computer['id'])+'">'+computer['identifier']+'</button></div>')

					#<a href="http://192.168.5.10/incidencias/frmnewext.php?login=pedcremo&idaula='+classroom_id+'&equipo='+computer['id']+'&serial='+str(computer['serial'])+'">I</a>
					
					#frmnewext.php?login=pedcremo&idaula=1&equipo=PC20&serial=SN3003030020
				else:
					response.write('<div id="computer-'+str(computer['id'])+'" class="ui-pc-forbidden"> ')
  					response.write('<img src="images/pc_mini_forbidden.png"/>')
  					response.write('<div class="desc"><button class="blockPC ui-button-pc-unlock" aula="aula-'+classroom_id+'" id="'+str(computer['id'])+'">'+computer['identifier']+'</button></div>')
  			elif computer['network_action']=="drop":
  					response.write('<div id="computer-'+str(computer['id'])+'" class="ui-pc-forbidden"> ')
  					response.write('<img src="images/pc_mini_forbidden.png"/>')
  					response.write('<div class="desc"><button class="blockPC ui-button-pc-unlock" aula="aula-'+classroom_id+'" id="'+str(computer['id'])+'">'+computer['identifier']+'</button></div>')
  			
  			else:
  					response.write('<div id="computer-'+str(computer['id'])+'" class="ui-pc-on"> ')
  					response.write('<img src="images/pc_mini.png"/>')
					response.write('<div class="desc"><button class="blockPC ui-button-pc-lock" aula="aula-'+classroom_id+'" id="'+str(computer['id'])+'">'+computer['identifier']+'</button></div>')
  			
  				
  			response.write("</div>")
  	except Exception, msg:  			
    		error_layer="ERROR: "+str(msg)
    		
  	
  	
  if error_layer:
  	response.write('<span class="ERROR" id="aula-'+ classroom_id+'">'+error_layer+'</span>')
  else:
  	response.write('<span class="hidden" id="aula-'+classroom_id+'"></span>')
  	
  response.write('</div>')
  return response
  
  
def draw_classroom(request,classroom_id,internet_id):
  response = HttpResponse()
  
  if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
 
  now = datetime.datetime.now()
  
  classroom_=Classroom.objects.get(id=classroom_id)
  
  #admin=classroom_.network_device.admin
  #password=classroom_.network_device.password
  #ip=classroom_.network_device.ip
  network_type=classroom_.network_device.network_type 
  
  mac_filter=classroom_.mac_filter
  firewall_rule=classroom_.firewall_rule
  
  #network_device_by_classroom= ApiNetworkDevice.objects.filter(id=classroom_net_device)

  if network_type=="Mikrotik":    
    try:
    	mk =MikrotikRouter()
    	mk.set_networkdevice(classroom_.network_device)
    	
    	mk.delete_classroom_firewall_rules(classroom_)
    	
    	if internet_id == "OFF":
		#mk.delete_firewall_rule("POST-LLISTA-"+classroom_id)
    		#mk.delete_firewall_rule("LLISTA-"+classroom_id)
		#If we filter classroom by mac because doesn't follow any IP range knowed 
    		if mac_filter:
			mk.block_classroom_by_mac(classroom_)
		else:    		
    			mk.add_firewall_rule(firewall_rule.comment,str(firewall_rule.src_address),str(firewall_rule.src_netmask))
    	else:
    		#mk.delete_firewall_rule(firewall_rule)
		if mac_filter:
			mk.delete_classroom_firewall_rules(classroom_)
    		else:
			mk.delete_firewall_rule(firewall_rule.comment)
    	
    	# Esborrem residus de regles parcials quan internet On or OFF
    	mk.delete_firewall_rule("POST-LLISTA-"+classroom_id)
    	mk.delete_firewall_rule("LLISTA-"+classroom_id)
    	
    except Exception, e:
    	response.write("ERROR: "+str(e))
    	
	
		
  return response
  #return direct_to_template(request, 'aules/aules.html')

def add_list_network_device(request,classroom_id,list_id):
  response = HttpResponse()  
  url_list = UrlList.objects.get(id=list_id)
  url_list_items = url_list.url_list_items.all()
  classroom_=Classroom.objects.get(id=classroom_id)
  network_type=classroom_.network_device.network_type 
  firewall_rule=classroom_.firewall_rule
  
  if network_type=="Mikrotik":
	try:
	  	mk =MikrotikRouter()
	  	mk.set_networkdevice(classroom_.network_device)
		mk.add_firewall_list(url_list_items,url_list.name)
				
		''' Add drop firewall rule'''
		mk.delete_firewall_rule("POST-LLISTA-"+classroom_id)

		#If we don't have other choice and we use the less preferable way to block a classroom. Blocking using every single MAC 		#from the PCs of the Classroom
		if classroom_.mac_filter:
			mk.block_classroom_by_mac(classroom_,"POST-LLISTA-"+classroom_id)
		else:
			mk.add_firewall_rule("POST-LLISTA-"+classroom_id,str(firewall_rule.src_address),str(firewall_rule.src_netmask))
		
		''' Add accept firewall rule to destination list'''
		mk.delete_firewall_rule("LLISTA-"+classroom_id)
		mk.add_firewall_rule("LLISTA-"+classroom_id,"","",url_list.name,"accept")
		
	except Exception, e:
    		response.write("ERROR: "+str(e))
		
  return response			

def remove_list_network_device(request,classroom_id):
  response = HttpResponse()  
  classroom_=Classroom.objects.get(id=classroom_id)
  network_type=classroom_.network_device.network_type 	
  if network_type=="Mikrotik":
	try:
	  	mk =MikrotikRouter()
	  	mk.set_networkdevice(classroom_.network_device)		
		mk.delete_firewall_rule("POST-LLISTA-"+classroom_id)
		mk.delete_firewall_rule("LLISTA-"+classroom_id)
		
	except Exception, e:
    		response.write("ERROR: "+str(e))
		
  return response
''' No estem fent cas a classroom_id HARDWIRED '''
def set_barra_lliure(request,classroom_id,barralliure_id):
  response = HttpResponse()
  classroom_=Classroom.objects.get(id=classroom_id)
  network_type=classroom_.network_device.network_type
  #response.write("set barra lliure") 
  if network_type=="Mikrotik":
        try:
                mk =MikrotikRouter()
                mk.set_networkdevice(classroom_.network_device)
    	        #response.write("ID barra lliure : "+classroom_id+" IS="+barralliure_id)
		if barralliure_id == "OFF":
	           #La regla 8 es srcnat per a l'aula 27 HARD WIRED
		   mk.enable_disable_firewall_nat_rule("src-nat-aula-27","0")
	
		else:
	           #La regla 8 es srcnat per a l'aula 27 HARD WIRED
		   mk.enable_disable_firewall_nat_rule("src-nat-aula-27","1")

        except Exception, e:
                response.write("EERROR: "+str(e))

  return response

''' Hardwired no fem cas del tot, de moment a classroom_id'''
def is_barra_lliure_set(classroom_id):
  classroom_=Classroom.objects.get(id=classroom_id)
  network_type=classroom_.network_device.network_type
  if network_type=="Mikrotik":
        try:
                mk =MikrotikRouter()
                mk.set_networkdevice(classroom_.network_device)
    	        
		return mk.is_firewall_nat_rule_enabled("src-nat-aula-27")
		

        except Exception, e:
                response.write("EERROR: "+str(e))

  return None
	


def forbidden(request):
   print "REQUEST "+str(request)
   return render_to_response('aules/forbidden.html')			
