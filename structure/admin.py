from structure.models import *
from stories.models import FeaturedStory
from django.contrib import admin

class IssueAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ('issue', 'volume', 'pub_date')}),
		('Structure', {'fields': ('sections', 'extra')})
	]
	
admin.site.register(Issue, IssueAdmin)
	
class SectionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ('name', 'short_name', 'slug')})
	]
	prepopulated_fields = {'short_name': ('name',),'slug': ('short_name',)}
	
admin.site.register(Section, SectionAdmin)
	
class VolumeAdmin(admin.ModelAdmin):
	pass

admin.site.register(Volume, VolumeAdmin)

class FlatPlanConfigAdmin(admin.ModelAdmin):
	list_display = ('name', 'list_sections')
	
admin.site.register(FlatPlanConfig, FlatPlanConfigAdmin)

class FeaturedInline(admin.TabularInline):
	model = FeaturedStory

class FrontPageConfigAdmin(admin.ModelAdmin):
	inlines = [
		FeaturedInline,
	]
	"""
	fieldsets = [
		(None, {'fields': ('pub_date', 'announce_head', 'announce_body', 'poll')}),
		('Featured', {'fields': ('featured')})
	]
	"""
	
admin.site.register(FrontPageConfig, FrontPageConfigAdmin)