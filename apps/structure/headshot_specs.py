from imagekit.specs import ImageSpec
from imagekit import processors

## Make sure you use this first for any ImageSpec
## Should preserve color errors when converting from CMYK
class MakeRGB(processors.Adjustment):
    color = 1.0

class ResizeThumb(processors.Resize):
    width = 100
    height = 100
    crop = True

class ResizeDisplay(processors.Resize):
    width = 200
    height = 100
    crop = True

class ResizeFront(processors.Resize):
    width = 225
    height = 150
    crop = True

class ResizeMobileFront(processors.Resize):
    width = 300
    height = 150
    crop = True

class EnhanceThumb(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1

class FrontImage(ImageSpec):
    access_as = 'front_image'
    pre_cache = True
    processors = [MakeRGB, ResizeFront, EnhanceThumb]

class Thumbnail(ImageSpec):
    access_as = 'thumbnail_image'
    pre_cache = True
    processors = [MakeRGB, ResizeThumb, EnhanceThumb]

class Display(ImageSpec):
    processors = [MakeRGB, ResizeDisplay]

class MobileFront(ImageSpec):
    access_as = 'mobile_front'
    processors = [MakeRGB, ResizeMobileFront]
