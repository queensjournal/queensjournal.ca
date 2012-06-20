import datetime
import factory
from video.models import Video


class VideoFactory(factory.Factory):
    FACTORY_FOR = Video

    name = "Test Video"
    slug = factory.Sequence(lambda n: "video%s" % n)
    pub_date = datetime.datetime.now() - datetime.timedelta(weeks=1)
    link = 'http://www.youtube.com/watch?v=xnxz3acXM6w'
    is_published = True
