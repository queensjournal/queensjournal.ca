from django.contrib import admin
from .models import Author, AuthorRole, Headshot


class AuthorRoleInline(admin.TabularInline):
    model = AuthorRole


class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        AuthorRoleInline,
    ]
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'bio', ]


class HeadshotAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)
admin.site.register(Headshot, HeadshotAdmin)
