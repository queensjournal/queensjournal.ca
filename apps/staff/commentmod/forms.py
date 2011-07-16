from django import forms
from comments.models import FreeComment

class SingleQuickActionForm(forms.Form):
    action = forms.CharField()
    comment = forms.IntegerField()
    url = forms.CharField()

    def clean_action(self):
        """
        Validates that the action is allowed by the system.
        """
        ACTIONS_ALLOWED = [
            'publish',
            'moderate',
            'delete',
            'undelete',
            ]
        if self.cleaned_data['action'] in ACTIONS_ALLOWED:
            return self.cleaned_data['action']
        raise forms.ValidationError(u'Improper comment action specified: %s' % self.cleaned_data['action'])

    def clean_comment(self):
        """
        Validates that the comment exists.
        """
        try:
            FreeComment.objects.get(pk=self.cleaned_data['comment'])
            return self.cleaned_data['comment']
        except:
            raise forms.ValidationError(u'Comment does not exist.')

    def clean_url(self):
        """
        Validates that the relative URL points to a list of comments.
        """
        import re
        urlprefix = re.compile('^/staff/comments/')
        if urlprefix.match(self.cleaned_data['url']):
            return self.cleaned_data['url']
        else:
            raise forms.ValidationError(u'Bad redirect URL after comment quickaction.')
