import operator
from django import template
from tagging.models import Tag
from tagging.utils import LINEAR

from stories.models import Story
from blog.models import Entry
from video.models import Video

register = template.Library()

def do_cloud():
    " returns a cloud "
    story_list = [tag for tag in Tag.objects.cloud_for_model(Story, steps=3,
        distribution=LINEAR, filters=None, min_count=None)]
    entry_list = [tag for tag in Tag.objects.cloud_for_model(Entry, steps=3,
        distribution=LINEAR, filters=None, min_count=None)]
    video_list = [tag for tag in Tag.objects.cloud_for_model(Video, steps=2,
        distribution=LINEAR, filters=None, min_count=None)]
    cloud = story_list + entry_list + video_list
    cloud.sort(lambda a, b: cmp(a.name, b.name))
    cloud1 = reduce(lambda l, x: x not in l and l.append(x) or l, cloud, [])
    return {'cloud': cloud1}

def popular_tags():
    " Top tags for a Thestar.com-style top topics bar. "
    story_list = Tag.objects.usage_for_model(Story, counts=True)
    entry_list = Tag.objects.usage_for_model(Entry, counts=True)
    video_list = Tag.objects.usage_for_model(Video, counts=True)
    tags = story_list + entry_list + video_list
    tags.sort(key=operator.attrgetter('count'), reverse=True)
    return {'tags': tags[:10]}

register.inclusion_tag('tags/tag_cloud.html')(do_cloud)
register.inclusion_tag('tags/popular_tags.html')(popular_tags)
