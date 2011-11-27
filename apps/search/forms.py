from django import forms
from django.db import models
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
import haystack
from haystack.forms import FacetedSearchForm

def model_choices(site=None):
    if site is None:
        site = haystack.site

    choices = [("%s.%s" % (m._meta.app_label, m._meta.module_name), capfirst(\
        unicode(m._meta.verbose_name_plural))) for m in site.get_indexed_models()]
    return sorted(choices, key=lambda x: x[1])

class SuperSearchForm(FacetedSearchForm):
    start_date = forms.DateField(required=False, widget=forms.HiddenInput)
    end_date = forms.DateField(required=False, widget=forms.HiddenInput)
    selected_facets = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(SuperSearchForm, self).__init__(*args, **kwargs)
        self.fields['models'] = forms.MultipleChoiceField(choices=model_choices(), \
            required=False, label=_('Search In'), widget=forms.CheckboxSelectMultiple)

    def get_models(self):
        """Return an alphabetical list of model classes in the index."""
        search_models = []

        if self.is_valid():
            for model in self.cleaned_data['models']:
                search_models.append(models.get_model(*model.split('.')))

        return search_models

    def search(self):
        sqs = super(SuperSearchForm, self).search()

        if hasattr(self, 'cleaned_data') and self.cleaned_data['selected_facets']:
            sqs = sqs.narrow(self.cleaned_data['selected_facets'])

        try:
            if self.cleaned_data['start_date']:
                sqs = sqs.filter(pub_date__gte=self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                sqs = sqs.filter(pub_date__lte=self.cleaned_data['end_date'])

        #Fallback in case someone accesses /search/ directly with no query
        except AttributeError:
            setattr(self, 'cleaned_data', '')

        return sqs.models(*self.get_models())
