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
	
class EnchanceThumb(processors.Adjustment): 
	contrast = 1.2 
	sharpness = 1.1
	
class Thumbnail(ImageSpec): 
	access_as = 'thumbnail_image' 
	pre_cache = True
	processors = [MakeRGB, ResizeThumb, EnchanceThumb] 

class Display(ImageSpec):
	processors = [MakeRGB, ResizeDisplay]