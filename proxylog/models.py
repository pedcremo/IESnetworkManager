from django.db import models

# Author Pere Crespo Molina

#In this class we are going to record Internet browsing habits 
"""
Examples strings sended by proxy

web-proxy,account 192.168.22.60 GET http://s.gravatar.com/js/gprofiles.js?aa&ver=3.3  action=allow cache=MISS

web-proxy,account 192.168.22.91 GET http://www.google.es/s?hl=es&gs_nf=3&pq=descargar%20open%20webos&cp=1&gs_id=16&xhr=t&q=dopen%20webos&pf=p&safe=active&client=ubuntu&hs=EyP&channel=fs&sclient=psy-ab&oq=&gs_l=&pbx=1&bav=on.2,or.r_gc.r_pw.r_qf.&fp=9 action=allow cache=MISS

web-proxy,account 192.168.22.55 POST http://evsecure-ocsp.verisign.com/  action=allow cache=MISS

web-proxy,account 192.168.22.140 GET http://www.cefe.gva.es/ite/privacitat/index_va.html  action=allow cache=MISS

Provat en rubular.com
---------------------
Expressio regular per fer match de la IP "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

Expressio regular per saber accio http "(GET|POST)"

Expressio regular per traure el domini "htt(p|ps):\/\/[a-z0-9.-]*" 

Per traure els parmetres de desprs del domini "htt(p|ps):\/\/[a-z0-9.-]*\/(\S*)" (2on grup de match)

Per traure action "action=(\S*)" (1er grup de match)

PEr traure cache  "cache=(\S*)" (1er grup de match)

"""

class ProxyEntry(models.Model):
	
	
	event_date = models.DateTimeField('DateTime event',blank=False,null=False)
	
	ip_src=models.GenericIPAddressField(verbose_name=u"Adreca IP font(src)",help_text="Adreca que fa la peticio",blank=False, null=False)
	
	ip_dst=models.GenericIPAddressField(verbose_name=u"Adreca IP desti(dst)",help_text="Adreca desti de la peticio",blank=True, null=True)
	
	
	domain_destination = models.CharField('Domain name', max_length=255,  blank=False, null=False)
	path = models.CharField('Path de la peticio', max_length=255, blank=True, null=True)

	action = models.CharField('action', max_length=10, blank=True, null=True)
	cache = models.CharField('cache', max_length=10, blank=True, null=True)

	computer_id = models.IntegerField('computer_id', blank=True, null=True)
