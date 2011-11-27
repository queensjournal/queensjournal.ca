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
class ResizeDisplay(processors.Resize):
    width = 150
    height = 150
    crop = True

# now lets create an adjustment processor to enhance the image at small sizes
class EnchanceThumb(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1

# now we can define our thumbnail spec
class Thumbnail(ImageSpec):
    access_as = 'thumbnail_image'
    pre_cache = True
    processors = [MakeRGB, ResizeThumb, EnchanceThumb]

# and our display spec
class Display(ImageSpec):
    quality = 85
    processors = [MakeRGB, ResizeDisplay]
