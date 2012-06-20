import datetime
from django.contrib import admin
from django.forms import ModelForm

from config.models import SiteConfig, FeaturedStory
from stories.models import Story


class FeaturedInlineForm(ModelForm):
    '''
    Limits the choices in the Featured Story Inline to cut down on database calls
    '''
    def __init__(self, *args, **kwargs):
        super(FeaturedInlineForm, self).__init__(*args, **kwargs)
        start_date = datetime.datetime.now() - datetime.timedelta(150)
        self.fields['story'].queryset = Story.objects.filter(
            pub_date__gte=start_date).order_by('-pub_date')


class FeaturedInline(admin.TabularInline):
    form = FeaturedInlineForm
    model = FeaturedStory


class ConfigAdmin(admin.ModelAdmin):
    inlines = [
        FeaturedInline,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(SiteConfig, ConfigAdmin)
