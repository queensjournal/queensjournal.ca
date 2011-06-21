import settings
from django.contrib import admin
from structure.models import Author
from galleries.models import PhotosPageOptions, Gallery

class PhotosPageAdmin(admin.ModelAdmin):
    filter_horizontal = ('photographers',)
    actions = None

    #def has_add_permission(self, request):
     #   return False
        
    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(PhotosPageOptions, PhotosPageAdmin)

class GalleryAdmin(admin.ModelAdmin):
    filter_horizontal = ['images']
    prepopulated_fields = {'slug': ('name',),}
    
    class Media:
        js = (settings.MEDIA_URL + 'js/admin/formatting-controls.js',)
        
admin.site.register(Gallery, GalleryAdmin)