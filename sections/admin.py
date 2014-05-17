from django.contrib import admin
from .models import Section


class SectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('name', 'short_name', 'slug')})
    ]
    prepopulated_fields = {'short_name': ('name',), 'slug': ('short_name',)}


admin.site.register(Section, SectionAdmin)

