from django.views.generic.detail import DetailView
from .models import Issue


class ArchiveIssueDetailView(DetailView):
    model = Issue
    template_name = 'archives/issue_detail.html'

    def get_object(self):
        return Issue.objects.get(volume__volume=self.kwargs['volume'],
                                 issue=self.kwargs['issue'])

issue_detail = ArchiveIssueDetailView.as_view()
