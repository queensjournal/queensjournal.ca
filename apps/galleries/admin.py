import settings
from django.contrib import admin
from structure.models import Author
from galleries.models import Gallery

class GalleryAdmin(admin.ModelAdmin):
    filter_horizontal = ['images']
    prepopulated_fields = {'slug': ('name',),}
    
    class Media:
        js = (settings.MEDIA_URL + 'js/admin/formatting-controls.js',)
        
admin.site.register(Gallery, GalleryAdmin)