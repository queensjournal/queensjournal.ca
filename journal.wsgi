import os
import sys
import site

from django.core.handlers.wsgi import WSGIHandler

# activate virtualenv
activate_this = os.path.expanduser("~/webapps/journal/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

site.addsitedir('/home/3781lanru0j/journal/lib/python2.7/site-packages')

sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
application = WSGIHandler()
