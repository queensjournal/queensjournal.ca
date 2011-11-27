# ImageKit options for story photos

from imagekit.specs import ImageSpec
from imagekit import processors

## Make sure you use this first for any ImageSpec
## Should preserve color errors when converting from CMYK
class MakeRGB(processors.Adjustment):
    color = 0.8

# now we define a display size resize processor
class ResizeDisplay(processors.Resize):
    width = 475
    height = 300
    crop = True

class ResizeMobile(processors.Resize):
    width = 620
    height = 350
    crop = True

# and our display spec
class Display(ImageSpec):
    quality = 85
    processors = [MakeRGB, ResizeDisplay]

class Mobile(ImageSpec):
    quality = 85
    processors = [MakeRGB, ResizeMobile]
