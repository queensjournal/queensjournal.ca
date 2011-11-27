from django.db import models
import datetime
from stories.models import Story, Photo


class Gallery(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    story = models.ForeignKey(Story, null=True, blank=True)
    pub_date = models.DateField()
    description = models.TextField()
    images = models.ManyToManyField(Photo, limit_choices_to = {
        'creation_date__gt': datetime.datetime.now() - datetime.timedelta(weeks=8)})

    class Meta:
        verbose_name = "Photo Gallery"
        verbose_name_plural = "Photo Galleries"

    def first_photo(self):
        try:
            return self.images.all()[0]
        except:
            return False

    @models.permalink
    def get_absolute_url(self):
        return ('galleries.views.gallery_detail', (), {
            'datestring': self.pub_date.strftime("%Y-%m-%d"),
            'slug': self.slug})

    def __unicode__(self):
        return self.name

    def list_authors(self):
        author_list = []
        for image in self.images.all():
            if not image.photographer in author_list and image.photographer is not None:
                author_list.append(image.photographer)
        author_num = len(author_list)
        authors = []
        for author in author_list:
            if author_num == 1:
                authors.append('<a href="/author/%s/">%s</a>, ' % (author.slug, author.name))
            else:
                authors.append('<a href="/author/%s/">%s</a>' % (author.slug, author.name))
        if author_num > 1:
            authors.insert(-1, 'and')
            authors.append('Journal Staff')
        elif author_num == 1:
            authors.append(author_list[0].get_role(self.pub_date))
        elif author_num == 0:
            authors.append('Journal Staff')
        return ' '.join(authors)
    list_authors.short_description = 'Author(s)'

