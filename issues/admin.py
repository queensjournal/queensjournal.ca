from django.contrib import admin
from .models import Issue, Volume


class VolumeAdmin(admin.ModelAdmin):
    pass


class IssueAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': (
            'issue',
            'volume',
            'pub_date',
            'is_published',
            )}),
        ('Structure', {'fields': ('sections', 'extra')})
    ]
    list_display = ('issue', 'pub_date', 'extra')
    list_filter = ['volume', ]


admin.site.register(Volume, VolumeAdmin)
admin.site.register(Issue, IssueAdmin)
