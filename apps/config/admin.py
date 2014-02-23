from django.contrib import admin
from django.forms import ModelForm
from solo.admin import SingletonModelAdmin
from selectable.forms.widgets import AutoCompleteSelectWidget

from stories.lookups import StoryLookup
from config.models import SiteConfig, FeaturedStory


class FeaturedStoryInlineForm(ModelForm):
    class Meta(object):
        model = FeaturedStory
        widgets = {
            'story': AutoCompleteSelectWidget(lookup_class=StoryLookup)
        }


class FeaturedInline(admin.TabularInline):
    model = FeaturedStory
    form = FeaturedStoryInlineForm
    extra = 1


class SiteConfigAdmin(SingletonModelAdmin):
    inlines = (
        FeaturedInline,
    )

admin.site.register(SiteConfig, SiteConfigAdmin)
