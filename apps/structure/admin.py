from structure.models import Issue, SectionFrontConfig, Section, Volume, FlatPlanSection,\
    FlatPlanConfig, FrontConfig, AuthorRole, Author, Headshot, FrontPageConfig
import datetime
from django.forms import ModelForm
from stories.models import FeaturedStory, Story
from django.contrib import admin

class IssueAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('issue', 'volume', 'pub_date')}),
        ('Structure', {'fields': ('sections', 'extra')})
    ]
    list_display = ('issue', 'pub_date', 'extra')
    list_filter = ['volume',]

admin.site.register(Issue, IssueAdmin)

class SectionConfigInline(admin.TabularInline):
    model = SectionFrontConfig

class SectionAdmin(admin.ModelAdmin):
    inlines = [ SectionConfigInline, ]
    fieldsets = [
        (None, {'fields': ('name', 'short_name', 'slug')})
    ]
    prepopulated_fields = {'short_name': ('name',),'slug': ('short_name',)}

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

class FeaturedInlineForm(ModelForm):
    '''
    Limits the choices in the Featured Story Inline to cut down on database calls
    '''
    def __init__(self, *args, **kwargs):
        super(FeaturedInlineForm, self).__init__(*args, **kwargs)
        start_date = datetime.datetime.now() - datetime.timedelta(150)
        self.fields['story'].queryset = Story.objects.filter(pub_date__gte=start_date).order_by('-pub_date')

class FeaturedInline(admin.TabularInline):
    form = FeaturedInlineForm
    model = FeaturedStory

class FrontConfigAdmin(admin.ModelAdmin):
    inlines = [
        FeaturedInline,
    ]

admin.site.register(FrontConfig, FrontConfigAdmin)

class AuthorRoleInline(admin.TabularInline):
    model = AuthorRole

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        AuthorRoleInline,
    ]
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'bio',]

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

''' OLD STUFF THAT DOESN'T REALLY NEED TO BE IN THE ADMIN
class AuthorRoleAdmin(admin.ModelAdmin):
	pass

admin.site.register(AuthorRole, AuthorRoleAdmin)

class FrontPageConfigAdmin(admin.ModelAdmin):
	pass

admin.site.register(FrontPageConfig, FrontPageConfigAdmin)
'''
