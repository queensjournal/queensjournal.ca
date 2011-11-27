# ImageKit options for story photos

from imagekit.specs import ImageSpec
from imagekit import processors

## Make sure you use this first for any ImageSpec
## Should preserve color errors when converting from CMYK
class MakeRGB(processors.Adjustment):
    color = 1.0

# first we define our thumbnail resize processor
class ResizeThumb(processors.Resize):
    width = 100
    height = 100
    crop = True

# now we define a display size resize processor
class ResizeList(processors.Resize):
    width = 475
    height = 300
    crop = False

class ResizeDetail(processors.Resize):
    width = 700
    height = 500
    crop = False

class ResizeFeatured(processors.Resize):
    width = 475
    height = 300
    crop = True

class ResizeGallery(processors.Resize):
    width = 800
    height = 600
    crop = False

# now lets create an adjustment processor to enhance the image at small sizes
class EnchanceThumb(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1

# now we can define our thumbnail spec
class Thumbnail(ImageSpec):
    access_as = 'thumbnail_image'
    processors = [MakeRGB, ResizeThumb, EnchanceThumb]

# and our display spec
class List(ImageSpec):
    quality = 85
    processors = [MakeRGB, ResizeList]

class Detail(ImageSpec):
    quality = 70
    processors = [MakeRGB, ResizeDetail]

class Featured(ImageSpec):
    quality = 75
    processors = [MakeRGB, ResizeFeatured]

class Gallery(ImageSpec):
    quality = 85
    access_as = "gallery_image"
    processors = [MakeRGB, ResizeGallery]
