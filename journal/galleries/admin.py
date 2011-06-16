from django.contrib import admin
from structure.models import Author
from galleries.models import PhotosPageOptions

class PhotosPageAdmin(admin.ModelAdmin):
    filter_horizontal = ('photographers',)
    actions = None

    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
    
admin.site.register(PhotosPageOptions, PhotosPageAdmin)