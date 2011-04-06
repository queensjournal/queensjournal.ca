from django.contrib import admin
import settings
from stories.models import Story, StoryPhoto, StoryAuthor, Photo, FeaturedPhoto
from inlines.models import Factbox, Document, StoryPoll
from galleries.models import Gallery

class GalleryInline(admin.TabularInline):
	model = Gallery
	extra = 1

class FactboxInline(admin.TabularInline):
	model = Factbox
	extra = 1
	
class DocumentInline(admin.TabularInline):
	model = Document
	extra = 1
	
class StoryPollInline(admin.TabularInline):
	model = StoryPoll
	extra = 1

class StoryPhotoInline(admin.TabularInline):
	model = StoryPhoto
	
class StoryAuthorInline(admin.TabularInline):
	model = StoryAuthor

class StoryAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,				 {'fields': ['head', 'deck', 'slug', 'label', 'tags', 'summary']}),
		('Date information', {'fields': ['pub_date']}),
		('Content', {'fields': ['content'], 'classes': ['richedit']}),
		('Organizational', {'fields': ['status', 'section', 'issue', 'featured',]})
	]
	inlines = [
		StoryPhotoInline,
		StoryAuthorInline,
		FactboxInline,
		DocumentInline,
		StoryPollInline,
		GalleryInline,
	]
	prepopulated_fields = {'slug': ('head',),}
	list_display = ('head', 'summary', 'pub_date', 'issue', 'featured', 'status')
	list_filter = ['pub_date', 'section', 'issue', 'status']
	search_fields = ['head', 'deck', 'content']
	actions = ['make_published', 'make_featured', 'remove_featured']
	
	class Media:
		js = (settings.MEDIA_URL + 'js/admin/formatting-controls.js',)
	
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
	search_fields = ['photo', 'name']
	list_display = ('name', 'issue', 'photographer', 'caption')
	
admin.site.register(Photo, PhotoAdmin)

class FeaturedPhotoAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	
admin.site.register(FeaturedPhoto, FeaturedPhotoAdmin)