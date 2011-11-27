from blog.models import Blog, BlogImage, Entry
from django.contrib import admin
import settings

class BlogImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(BlogImage, BlogImageAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',),}
    filter_horizontal = ('bloggers',)

admin.site.register(Blog, BlogAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display        = ('title','author','pub_date','date_saved', 'is_published')
    list_filter         = ('blog','pub_date','is_published')
    search_fields       = ('title','content')
    prepopulated_fields = {'slug': ('title',),}
    fieldsets = [
        ('Top matter', {'fields': ('title','blog','author','slug','tags')}),
        ('Publish settings', {'fields': ('is_published','pub_date')}),
        ('Content', {'fields': ['content'], 'classes': ['richedit']}),
        ('Discussion', {'fields': ('enable_comments',)}),
        ]

    class Media:
        js = (settings.MEDIA_URL + 'js/admin/formatting-controls.js',)

admin.site.register(Entry, EntryAdmin)
