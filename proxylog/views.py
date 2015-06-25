# Create your views here.
from django.shortcuts import render_to_response,render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
#from django.views.generic.simple import direct_to_template
from pprint import PrettyPrinter
from proxylog.models import ProxyEntry
from aules.models import Classroom
from django.db.models import Count
import datetime

""" LES 30 WEBS MES VISITADES DE AULA 21
---------------------------------------
SELECT COUNT( * ) AS hits, domain_destination
FROM  `proxylog_proxyentry` 
WHERE ip_src LIKE  "192.168.21%"
GROUP BY domain_destination
ORDER BY hits DESC 
LIMIT 0 , 30 """

def top30(request,classroom_id,minutes_="ALL"):
	classroom=Classroom.objects.get(id=classroom_id)
	
	if (classroom.name.endswith("21")):
		ip_regex="192.168.21"
	elif (classroom.name.endswith("22")):
		ip_regex="192.168.22"
	elif (classroom.name.endswith("23")):
		ip_regex="192.168.23"
	elif (classroom.name.endswith("26")):
		ip_regex="192.168.26"
	elif (classroom.name.endswith("27")):
		ip_regex="192.168.27"
	elif (classroom.name.endswith("28")):
		ip_regex="192.168.28"
	elif (classroom.name.endswith("20")):
		ip_regex="192.168.11"
	else:
		ip_regex="192.168.5"

	if (minutes_=="ALL"):
 	    url_proxy_list = ProxyEntry.objects.filter(ip_src__startswith=ip_regex).values('domain_destination').order_by('-domain_destination__count').annotate(Count('domain_destination'))[:30]
	#Easter EGG
	elif (minutes_=="666"): 
	    url_proxy_list = ProxyEntry.objects.filter(ip_src__startswith="192.168").values('domain_destination').order_by('-domain_destination__count').annotate(Count('domain_destination'))[:30]
	    moment ="Qualsevol moment TOT INSTITUT"		
	else:
	    created_time = datetime.datetime.now() - datetime.timedelta(minutes=int(minutes_))
            url_proxy_list = ProxyEntry.objects.filter(ip_src__startswith=ip_regex).filter(event_date__gte=created_time).values('domain_destination').order_by('-domain_destination__count').annotate(Count('domain_destination'))[:30]
		
	if (minutes_=="ALL"):
		moment="Qualsevol moment"
	elif (minutes_=="5"):
		moment="Darrers 5 minuts"
	elif (minutes_=="30"):
		moment="Darrers 30 minuts"
	elif (minutes_=="60"):
		moment="Darrera hora"
	elif (minutes_=="1440"):
		moment="Darrer dia"
	elif (minutes_=="10080"):
		moment="Darrera setmana"
	elif (minutes_=="43200"):
		moment="Darrer mes"

	return render_to_response('proxylog/index.html', {'classroom_name':classroom.name,'classroom_id':classroom_id, 'ip_network':ip_regex,'url_proxy_list': url_proxy_list,'moment':moment},context_instance=RequestContext(request))
	
