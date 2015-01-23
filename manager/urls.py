from django.conf.urls import patterns, include, url
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

APPLICATION_DIR= os.path.split(os.path.abspath(os.path.split(os.path.abspath(__file__))[0]))[0]

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'manager.views.home', name='home'),
    # url(r'^manager/', include('manager.foo.urls')),
    url(r'^$', 'aules.views.index',name='home'),
    url(r'^forbidden/$', 'aules.views.forbidden',name='forbidden'),	
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'aules/login.html'},name='login'),
    url(r'^login_check/$', 'aules.views.mylogin'),
    url(r'^logout/$', 'aules.views.mylogout'),	
    url(r'^draw_classroom/aula-(?P<classroom_id>\d+)/(?P<internet_id>ON|OFF)/$', 'aules.views.draw_classroom'),	
    url(r'^drawing_classroom/aula-(?P<classroom_id>\d+)/(?P<internet_id>ON|OFF|INFO)/$', 'aules.views.drawing_classroom'),	
    url(r'^block_by_mac/(?P<pc_id>\d+)/(?P<pc_state>ON|OFF)/$', 'aules.views.block_by_mac'),	
    url(r'^allow_by_mac/(?P<pc_id>\d+)/(?P<pc_state>ON|OFF)/$', 'aules.views.allow_by_mac'),
    url(r'^add_list_network_device/aula-(?P<classroom_id>\d+)/(?P<list_id>\d+)/$', 'aules.views.add_list_network_device'),
    url(r'^remove_list_network_device/aula-(?P<classroom_id>\d+)/$', 'aules.views.remove_list_network_device'),
    url(r'^set_barra_lliure/aula-(?P<classroom_id>\d+)/(?P<barralliure_id>ON|OFF)/$','aules.views.set_barra_lliure'),
    #url(r'^draw_classroom/aula-(?P<classroom_id>\d+)/$', 'aules.views.draw_classroom'),	
      
    #Proxy log routes
    url(r'^proxylog/aula-(?P<classroom_id>\d+)/$', 'proxylog.views.top30'),		
    url(r'^proxylog/aula-(?P<classroom_id>\d+)/last-(?P<minutes_>\d+)-minutes$', 'proxylog.views.top30'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
     
    (r'^jquery/(?P<path>.*)$', 'django.views.static.serve',
                 { 'document_root': os.path.join( APPLICATION_DIR,"aules/js/jquery") }),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
                 { 'document_root': os.path.join( APPLICATION_DIR,"aules/static/images") }),
    (r'^forbidden/images/(?P<path>.*)$', 'django.views.static.serve',
                 { 'document_root': os.path.join( APPLICATION_DIR,"aules/static/images") }),	
    
)
