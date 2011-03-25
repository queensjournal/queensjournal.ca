from django import forms
from polls.models import Choice

class PollVotingForm(forms.Form):
    """
    Form for selecting an option from a poll and adding one vote to it.
    """
    def __init__(self, poll, *args, **kwargs):
        super(PollVotingForm, self).__init__(*args, **kwargs)
        self.poll = poll
        self.fields['choice']._set_choices([(x.id, x.choice) for x in Choice.objects.filter(poll__id=self.poll)])

    choice = forms.ChoiceField(widget=forms.RadioSelect)
