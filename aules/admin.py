from aules.models import Classroom
from aules.models import Computer
from aules.models import PCmodel
from aules.models import ApiNetworkDevice
from aules.models import FirewallRule
from aules.models import UrlList
from aules.models import UrlListItem
from django.contrib import admin

class ComputerInline(admin.TabularInline):
	model = Computer
	extra = 18
	
class UrlListInline(admin.TabularInline):
	model = UrlListItem
	extra = 5

class ClassroomAdmin(admin.ModelAdmin):
	inlines=[ComputerInline]

class UrlListAdmin(admin.ModelAdmin):
	inlines=[UrlListInline]


admin.site.register(Classroom,ClassroomAdmin)
admin.site.register(Computer)
admin.site.register(PCmodel)
admin.site.register(ApiNetworkDevice)
admin.site.register(FirewallRule)
#admin.site.register(UrlList,UrlListAdmin)
admin.site.register(UrlList)
admin.site.register(UrlListItem)
