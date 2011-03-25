from structure.models import *
from stories.models import FeaturedStory, FeaturedPhoto, Section, Story
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

class FlatPlanSectionInline(admin.TabularInline):
	model = FlatPlanSection

class FlatPlanConfigAdmin(admin.ModelAdmin):
	list_display = ('name', 'list_sections')
	inlines = [
		FlatPlanSectionInline,
	]
	
admin.site.register(FlatPlanConfig, FlatPlanConfigAdmin)

class FeaturedInline(admin.TabularInline):
	model = FeaturedStory
	ordering = ['pub_date']

class FrontConfigAdmin(admin.ModelAdmin):
	inlines = [
		FeaturedInline,
	]
	"""
	fieldsets = [
		(None, {'fields': ('pub_date', 'announce_head', 'announce_body', 'poll')}),
		('Featured', {'fields': ('featured')})
	]
	"""
	
admin.site.register(FrontConfig, FrontConfigAdmin)
	
class SectionFrontConfigAdmin(admin.ModelAdmin):
	"""
	fieldsets = [
		(None, {'fields': ('pub_date', 'announce_head', 'announce_body', 'poll')}),
		('Featured', {'fields': ('featured')})
	]
	"""
	actions = None
	
admin.site.register(SectionFrontConfig, SectionFrontConfigAdmin)