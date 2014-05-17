from django import forms
from images.models import Image

class ImageForm(forms.Form):
    name = forms.CharField()
    image = forms.ImageField()
    caption = forms.CharField(widget=forms.Textarea, required=False)
    credit = forms.CharField(required=False)

    def clean_name(self):
        if self.cleaned_data.get('name') and Image.objects.filter(name = \
            self.cleaned_data['name']).count() != 0:
            raise forms.ValidationError(u'An image object with this name already exists. \
                Please use a different name.')
        return self.cleaned_data['name']
