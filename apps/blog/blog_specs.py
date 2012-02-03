# ImageKit options for story photos

from imagekit.specs import ImageSpec
from imagekit import processors

## Make sure you use this first for any ImageSpec
## Should preserve color errors when converting from CMYK
class MakeRGB(processors.Adjustment):
    color = 1.0

class HeaderColor(processors.Adjustment):
    color = 0.3
    contrast = 0.8

# first we define our thumbnail resize processor
class ResizeThumb(processors.Resize):
    width = 200
    height = 30
    crop = True

# now we define a display size resize processor
class ResizeHeader(processors.Resize):
    width = 720
    height = 100
    crop = True

class ResizeFront(processors.Resize):
    width = 225
    height = 150
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
class Header(ImageSpec):
    quality = 85
    access_as = "header_image"
    processors = [HeaderColor, ResizeHeader]

class Front(ImageSpec):
    quality = 85
    access_as = "front_image"
    processors = [MakeRGB, ResizeFront]
