from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify

class Image(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text='Descriptive name of the image. Will be displayed as alt text.')
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='content/%Y/%m/')
##    thumb = models.ImageField(upload_to='thumbs/%Y/%m/', editable=False)
    caption = models.TextField(blank=True, help_text='Caption for the image. Optional.')
    credit = models.CharField(max_length=64, blank=True, help_text='Image credit. Optional.')
    date_added = models.DateTimeField(default=datetime.now,editable=False)

    class Admin:
        list_display =          ('name','get_image_url',)

    def __unicode__(self):
        return self.name

    def rename(self, image, newfilename):
        """
        Renames images to the specified filename.
        """
        import shutil
        import os
        import re
        from os import path
        from django.conf import settings
        # grab path, filename, extension
        pathname, filename = path.split(image)
        extension = path.splitext(filename)[1]
        # create new filename
        newname = '%s%s' % (newfilename, extension)
        if filename != newname:
            new_location = path.join(settings.MEDIA_ROOT, pathname, newname)
            old_location = path.join(settings.MEDIA_ROOT, image)
            if new_location != old_location:
                shutil.move(old_location, new_location)
            return path.join(pathname, newname)
        else:
            return image

    def save(self):
        from os import path
        if self.slug == '' or self.slug is None:
            self.slug = slugify(self.name)[0:49]
        self.image = self.rename(self.image, self.slug)
##
##        if not self.thumb:
##            from PIL import Image as PILImage
##            # Set our max thumbnail size in a tuple (max width, max height)
##            THUMBNAIL_SIZE = (128, 128)
##        
##            # Save fake thumbnail as empty so we can get the filename from the 
##            # original filename, from Django's convenience method 
##            # get_FIELD_filename()
##            self.save_thumb_file(self.get_image_filename(), '')
##        
##            # Open original photo which we want to thumbnail using PIL's Image
##            # object
##            image = PILImage.open(self.get_image_filename())
##        
##            # We use our PIL Image object to create the thumbnail, which already
##            # has a thumbnail() convenience method that contrains proportions.
##            # Additionally, we use Image.ANTIALIAS to make the image look better.
##            # Without antialiasing the image pattern artifacts may result.
##            image.thumbnail(THUMBNAIL_SIZE, PILImage.ANTIALIAS)
##        
##            # Save the thumbnail
##            image.save(self.get_thumb_filename())
##
        # Save this photo instance
        super(Image, self).save()
