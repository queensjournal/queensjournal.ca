from django.contrib import admin
from sidelinks.models import SidebarLinkset, Link

class SidelinkInline(admin.TabularInline):
	model = Link
	fields = ['text', 'link', 'css_class']

class SidebarAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	inlines = [
		SidelinkInline,
	]
	
admin.site.register(SidebarLinkset, SidebarAdmin)