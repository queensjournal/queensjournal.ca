from urllib import unquote
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from stories.models import Story
from blog.models import Entry
from video.models import Video
from tagging.models import TaggedItem, Tag
from dependencies.multiquery import QuerySetChain


def tags(request):
    return render_to_response("tags/tags.html", context_instance=RequestContext(request))

def with_tag(request, tag, object_id=None, page=1):
    unslug = unquote(tag)
    query_tag = get_object_or_404(Tag, name=unslug)
    story_list = TaggedItem.objects.get_by_model(Story, query_tag).order_by('-pub_date')
    entry_list = TaggedItem.objects.get_by_model(Entry, query_tag).order_by('-pub_date')
    video_list = TaggedItem.objects.get_by_model(Video, query_tag).order_by('-pub_date')
    result_list = QuerySetChain(story_list, entry_list, video_list)
    return render_to_response("tags/with_tag.html", {'tag': unslug,
                                'stories': result_list},
                                context_instance=RequestContext(request))
