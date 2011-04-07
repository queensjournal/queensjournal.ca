from structure.models import *
from stories.models import FeaturedStory, Section, Story
from django.contrib import admin

class IssueAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ('issue', 'volume', 'pub_date')}),
		('Structure', {'fields': ('sections', 'extra')})
	]
	list_display = ('issue', 'pub_date', 'extra')
	
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
	list_display = ('section',)
	
admin.site.register(SectionFrontConfig, SectionFrontConfigAdmin)

class AuthorRoleInline(admin.TabularInline):
	model = AuthorRole

class AuthorAdmin(admin.ModelAdmin):
	inlines = [
		AuthorRoleInline,
	]
	list_display = ('name',)
	prepopulated_fields = {'slug': ('name',)}
	search_fields = ['name', 'bio',]
	
admin.site.register(Author, AuthorAdmin)

class HeadshotAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Headshot, HeadshotAdmin)

class AuthorRoleAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(AuthorRole, AuthorRoleAdmin)


class FrontPageConfigAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(FrontPageConfig, FrontPageConfigAdmin)