from django.contrib import admin
from sidelinks.models import SidebarLinkset, Link

class SidelinkInline(admin.TabularInline):
	model = Link

class SidebarAdmin(admin.ModelAdmin):
	inlines = [
		SidelinkInline,
	]
	
admin.site.register(SidebarLinkset, SidebarAdmin)