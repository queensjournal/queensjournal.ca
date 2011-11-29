import settings
from django.contrib import admin
from galleries.models import Gallery

class GalleryAdmin(admin.ModelAdmin):
    filter_horizontal = ['images']
    list_display = ['name', 'pub_date']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',),}

    class Media:
        js = (settings.MEDIA_URL + 'js/admin/formatting-controls.js',)

admin.site.register(Gallery, GalleryAdmin)
