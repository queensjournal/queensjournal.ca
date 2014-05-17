from django.views.generic.detail import DetailView
from stories.models import Story


class StoryDetailView(DetailView):

    model = Story

    def get_queryset(self):
        return Story.objects.published()

story_detail = StoryDetailView.as_view()
