from structure.models import Issue, SectionFrontConfig, Section, Volume, FlatPlanSection,\
    FlatPlanConfig, AuthorRole, Author, Headshot, FrontPageConfig
from django.contrib import admin


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

admin.site.register(Issue, IssueAdmin)


class SectionConfigInline(admin.TabularInline):
    model = SectionFrontConfig


class SectionAdmin(admin.ModelAdmin):
    inlines = [SectionConfigInline, ]
    fieldsets = [
        (None, {'fields': ('name', 'short_name', 'slug')})
    ]
    prepopulated_fields = {'short_name': ('name',), 'slug': ('short_name',)}


admin.site.register(Section, SectionAdmin)


class VolumeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Volume, VolumeAdmin)


class FlatPlanSectionInline(admin.TabularInline):
    model = FlatPlanSection


class FlatPlanConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'list_sections')
    inlines = [
        FlatPlanSectionInline,
    ]


admin.site.register(FlatPlanConfig, FlatPlanConfigAdmin)


class AuthorRoleInline(admin.TabularInline):
    model = AuthorRole


class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        AuthorRoleInline,
    ]
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'bio', ]


admin.site.register(Author, AuthorAdmin)


class HeadshotAdmin(admin.ModelAdmin):
    pass


admin.site.register(Headshot, HeadshotAdmin)


class FrontPageConfigAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False


admin.site.register(FrontPageConfig, FrontPageConfigAdmin)
