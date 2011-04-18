from django import forms
from haystack.forms import SearchForm, ModelSearchForm

class SuperSearchForm(ModelSearchForm):
	start_date = forms.DateField(required=False, widget=forms.HiddenInput)
	end_date = forms.DateField(required=False, widget=forms.HiddenInput)
	selected_facets = forms.CharField(required=False, widget=forms.HiddenInput)
	
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