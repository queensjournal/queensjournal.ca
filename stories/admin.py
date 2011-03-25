from django.contrib import admin
from stories.models import Story, StoryPhoto, FeaturedPhoto, Photo

class StoryPhotoInline(admin.TabularInline):
	model = StoryPhoto

class StoryAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,				 {'fields': ['head', 'kick', 'slug', 'label']}),
		('Date information', {'fields': ['pub_date']}),
		('Content', {'fields': ['summary','content']}),
		('Organizational', {'fields': ['status', 'section', 'issue', 'featured', 'tags']})
	]
	inlines = [
		StoryPhotoInline,
	]
	prepopulated_fields = {'slug': ('head',)}
	list_display = ('head', 'summary', 'pub_date', 'issue')
	list_filter = ['pub_date', 'section', 'issue']
	search_fields = ['question']
	actions = ['make_published', 'make_featured', 'remove_featured']
	
	def make_published(self, request, queryset):
		rows_updated = queryset.update(featured=True)
		if rows_updated == 1:
			message_bit = "1 story was"
		else:
			message_bit = "%s stories were" % rows_updated
		self.message_user(request, "%s successfully marked as published." % message_bit)
	make_published.short_description = "Mark selected stories as published"
		
	def make_featured(self, request, queryset):
		rows_updated = queryset.update(featured=True)
		if rows_updated == 1:
			message_bit = "1 story was"
		else:
			message_bit = "%s stories were" % rows_updated
		self.message_user(request, "%s successfully marked as featured." % message_bit)
	make_featured.short_description = "Mark selected stories as featured"
	
	def remove_featured(self, request, queryset):
		rows_updated = queryset.update(featured=False)
		if rows_updated == 1:
			message_bit = "1 story was"
		else:
			message_bit = "%s stories were" % rows_updated
		self.message_user(request, "%s successfully removed from featured." % message_bit)
	remove_featured.short_description = "Remove selected from featured"

admin.site.register(Story, StoryAdmin)

class PhotoAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	
admin.site.register(Photo, PhotoAdmin)

class FeaturedPhotoAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	
admin.site.register(FeaturedPhoto, FeaturedPhotoAdmin)