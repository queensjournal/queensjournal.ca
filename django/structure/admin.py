from structure.models import *
import datetime
from django.forms import ModelForm
from stories.models import FeaturedStory, Section, Story
from django.contrib import admin

class IssueAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ('issue', 'volume', 'pub_date')}),
		('Structure', {'fields': ('sections', 'extra')})
	]
	list_display = ('issue', 'pub_date', 'extra')
	list_filter = ['volume',]
	
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

class FeaturedInlineForm(ModelForm):
	'''
	Limits the choices in the Featured Story Inline to cut down on database calls
	'''
	def __init__(self, *args, **kwargs):
		super(FeaturedInlineForm, self).__init__(*args, **kwargs)
		start_date = datetime.datetime.today() - datetime.timedelta(150)
		self.fields['story'].queryset = Story.objects.filter(pub_date__range=(start_date, datetime.datetime.today())).order_by('-pub_date')

class FeaturedInline(admin.TabularInline):
	form = FeaturedInlineForm
	model = FeaturedStory

class FrontConfigAdmin(admin.ModelAdmin):
	inlines = [
		FeaturedInline,
	]
	
admin.site.register(FrontConfig, FrontConfigAdmin)
	
class SectionFrontConfigAdmin(admin.ModelAdmin):
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