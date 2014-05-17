from django.views.generic.detail import DetailView

from .models import Section


class SectionDetailView(DetailView):
    model = Section

section_detail = SectionDetailView.as_view()
