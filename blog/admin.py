from blog.models import Blog, EntryManager, Entry, Category
from structure.models import Author
from django.contrib import admin

class BlogAdmin(admin.ModelAdmin):
	list_display = ('title',)
	prepopulated_fields = {'slug': ('title',),}
	filter_horizontal = ('bloggers',)
	
admin.site.register(Blog, BlogAdmin)

class EntryAdmin(admin.ModelAdmin):
	list_display        = ('title','author','date_published','date_saved')
	list_filter         = ('blog','date_published','is_published','categories')
	search_fields       = ('title','content')
	prepopulated_fields = {'slug': ('title',),}
	filter_horizontal = ('categories',)
	fieldsets = [
	   	('Top matter', {'fields': ('title','blog','author','slug')}),
	    ('Publish settings', {'fields': ('is_published','date_published')}),
	    ('Content', {'fields': ('categories','content')}),
	    ('Discussion', {'fields': ('enable_comments',)}),
	    ]
	
admin.site.register(Entry, EntryAdmin)