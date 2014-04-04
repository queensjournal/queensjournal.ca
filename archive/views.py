import datetime

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from issues.models import Volume, Issue


class ArchiveVolumeListView(ListView):
    model = Volume
    template_name = 'archives/volume_list.html'

archive_volume_list = ArchiveVolumeListView.as_view()


class ArchiveVolumeDetailView(DetailView):
    model = Volume
    slug_field = 'volume'
    slug_url_kwarg = 'volume'
    template_name = 'archives/volume_detail.html'

archive_volume_detail = ArchiveVolumeDetailView.as_view()


def legacy_archive_issue_detail(request, year, month, day):
    date = datetime.date(int(year), int(month), int(day))
    return redirect(Issue.objects.get(pub_date=date).get_absolute_url(),
        permanent=True)
