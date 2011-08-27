from django.forms import ModelForm
from staff.requests.models import PhotoRequest

class RequestForm(ModelForm):
    class Meta:
        model = PhotoRequest
        fields = ('subject', 'location', 'time', 'section', 'deadline', 'notes', 'status', )