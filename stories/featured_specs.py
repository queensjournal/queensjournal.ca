# ImageKit options for story photos

from imagekit.specs import ImageSpec 
from imagekit import processors 

# now we define a display size resize processor
class ResizeDisplay(processors.Resize):
	width = 700
	height = 300
	crop = True

# and our display spec
class Display(ImageSpec):
	processors = [ResizeDisplay]