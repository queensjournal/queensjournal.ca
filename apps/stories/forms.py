from django import forms

required = {'class': 'required'}

class EmailStoryForm(forms.Form):
    sender = forms.CharField(max_length=255,
                             widget=forms.TextInput(attrs=required))
    email = forms.EmailField(widget=forms.TextInput(attrs=required))
    message = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows':10,'cols':60}))
