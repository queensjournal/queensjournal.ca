from django.contrib import admin
from video.models import Video
import settings

class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}
    search_fields = ['name', 'caption', 'photographer']
    list_display = ('name', 'photographer', 'pub_date', 'tags',)

    class Media:
        js = (settings.MEDIA_URL + 'js/admin/formatting-controls.js',)

admin.site.register(Video, VideoAdmin)
