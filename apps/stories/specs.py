# ImageKit options for story photos

from imagekit.specs import ImageSpec
from imagekit import processors

## Make sure you use this first for any ImageSpec
## Should preserve color errors when converting from CMYK
class MakeRGB(processors.Adjustment):
    color = 0.8

# first we define our thumbnail resize processor
class ResizeThumb(processors.Resize):
    width = 100
    height = 100
    crop = True

# now we define a display size resize processor
class ResizeDisplay(processors.Resize):
    width = 475
    height = 300
    crop = True

class ResizeFront(processors.Resize):
    width = 225
    height = 150
    crop = True

class ResizeMobileFront(processors.Resize):
    width = 300
    height = 150
    crop = True

class ResizeGallery(processors.Resize):
    width = 800
    height = 600
    crop = False

class ResizeGalleryFeatured(processors.Resize):
    width = 720
    height = 480
    crop = True

class ResizeFirst(processors.Resize):
    width = 700
    height = 500
    crop = False

class ResizeOther(processors.Resize):
    width = 430
    height = 600
    crop = False

class ResizeMobile(processors.Resize):
    width = 620
    height = 410
    crop = True

class ResizeMobileFeatured(processors.Resize):
    width = 620
    height = 350
    crop = True

# now lets create an adjustment processor to enhance the image at small sizes
class EnchanceThumb(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1

# now we can define our thumbnail spec
class Thumbnail(ImageSpec):
    access_as = 'thumbnail_image'
    processors = [MakeRGB, ResizeThumb, EnchanceThumb]

# and our display spec
class Display(ImageSpec):
    quality = 85
    processors = [MakeRGB, ResizeDisplay]

class Front(ImageSpec):
    quality = 85
    access_as = "front_image"
    processors = [MakeRGB, ResizeFront]

class MobileFront(ImageSpec):
    quality = 75
    access_as = "mobile_front"
    processors = [MakeRGB, ResizeMobileFront]

class Gallery(ImageSpec):
    quality = 85
    access_as = "gallery_image"
    processors = [MakeRGB, ResizeGallery]

class GalleryFeatured(ImageSpec):
    access_as = 'gallery_featured'
    processors = [MakeRGB, ResizeGalleryFeatured]

class Other(ImageSpec):
    access_as = 'other'
    processors = [MakeRGB, ResizeOther]

class First(ImageSpec):
    access_as = 'first'
    processors = [MakeRGB, ResizeFirst]

class Mobile(ImageSpec):
    access_as = 'mobile'
    processors = [MakeRGB, ResizeMobile]

class MobileFeatured(ImageSpec):
    access_as = 'mobile_featured'
    processors = [MakeRGB, ResizeMobileFeatured]
