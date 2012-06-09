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

    #def setup_video_tests(self):
        #super(VideoTestHelper, self).setUp()
        #test_image_source = os.path.join(settings.DJANGO_ROOT, 'tests/test.jpg')
        #self.test_image_dest = 'test_data/test.jpg'
        #shutil.copy(test_image_source, os.path.join(settings.MEDIA_ROOT, self.test_image_dest))

    #def create_video(self, **kwargs):
        #self.setup_video_tests()
        #defaults = {
            #'name': u'Test Video',
            #'slug': 'video1',
            #'link': u'http://www.youtube.com/watch?v=xnxz3acXM6w',
            #'caption': u'Get it pregnant!',
            #'photographer': self.create_author(),
            #'screenshot': self.test_image_dest,
            #'is_published': True,
        #}
        #defaults.update(kwargs)
        #obj, created = Video.objects.get_or_create(**defaults)
        #return obj
