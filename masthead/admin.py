from django.contrib import admin
from masthead.models import MastheadName, Masthead

class MastheadInline(admin.TabularInline):
    model = MastheadName

class MastheadAdmin(admin.ModelAdmin):
    inlines = [
        MastheadInline,
        ]

admin.site.register(Masthead, MastheadAdmin)
