from django import forms
from blog.models import Blog, Entry, Category, AuthorProfile

class AjaxPreviewForm(forms.Form):
    blog = forms.ChoiceField(choices=[(x.id,x.title) for x in Blog.objects.all()])
    title = forms.CharField()
    content = forms.CharField()
    author = forms.IntegerField()
    categories = forms.MultipleChoiceField(choices=[(x.id,x.name) for x in Category.objects.all()], required=False)

    def clean_author(self):
        try:
            AuthorProfile.objects.get(pk=self.cleaned_data['author'])
            return self.cleaned_data['author']
        except:
            raise ValidationError(u'Improper author specified!')


class ProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    homepage = forms.URLField(required=False)
    portrait = forms.ImageField(required=False)
    #portrait_delete = forms.BooleanField(required=False, initial=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput, required=False)

    def clean_password2(self):
        if self.cleaned_data.get('password1') and self.cleaned_data.get('password2') and self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(u'Please make sure your passwords match.')
        return self.cleaned_data['password2']
