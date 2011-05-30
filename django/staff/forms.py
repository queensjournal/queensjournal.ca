from django import forms
from django.contrib.auth.models import User

attrs_dict = { 'class': 'required' }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs=attrs_dict),
                               label=u'Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
                                label=u'Password')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
                                label=u'Old password')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
                                label=u'New password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
                                label=u'Repeat new password (to catch typos)')

    def clean_password2(self):
        """
        Validates that the two password inputs match.
        
        """
        if self.clean_data.get('password1', None) and self.clean_data.get('password2', None) and \
           self.clean_data['password1'] == self.clean_data['password2']:
            return self.clean_data['password2']
        raise forms.ValidationError(u'You must type the same password each time')
