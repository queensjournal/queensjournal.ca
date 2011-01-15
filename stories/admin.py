from stories.models import Story
from django.contrib import admin

class StoryAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['head', 'kick', 'slug', 'label']}),
		('Date information', {'fields': ['pub_date']}),
		('Content', {'fields': ['summary','content']}),
		('Organizational', {'fields': ['published', 'front', 'section', 'issue', 'twitter']})
	]
	prepopulated_fields = {'slug': ('head',)}
	list_display = ('head', 'pub_date', 'issue')
	list_filter = ['pub_date','issue']
	search_fields = ['question']
	date_hierarchy = 'pub_date'

admin.site.register(Story, StoryAdmin)