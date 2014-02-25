import re
from django import template
from django.template import Context, Template
from django.template.loader import get_template
from images.models import Image

register = template.Library()

def images(value, spec):
    """
    Detects <!--image:"slug-field"--> tags and replaces them with an
    image template containing the proper image. max_width parameter in pixels.

    {{ content|...filters here...|images:430 }}
    """
    t = get_template('images/image_instance.html')
    stubs_re = re.compile('<!--image:"([-\w]+)"-->',re.IGNORECASE)
    for stub in stubs_re.findall(value):
        try:
            image = Image.objects.get(slug__exact=stub)
        except:
            continue
        c = Context({'image': image, 'spec': spec})
        image_re = re.compile('<!--image:"'+stub+'"-->')
        value = image_re.sub(t.render(c), value)
    return value

register.filter(images)
