"""
To function this requires the following to be installed:

TEMPLATE_CONTEXT_PROCESSORS
django.core.context_processors.request

MIDDLEWARE_CLASSES
django.contrib.sessions.middleware.SessionMiddleware

@author: Robert Conner (rtconner)
"""

from django import template
import datetime
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.conf import settings

register = template.Library()


def session_clear(session):
    """
    Private function, clear flash msgsfrom the session
    """
    try:
        del session['flash_msg']
    except KeyError:
        pass

    try:
        del session['flash_params']
    except KeyError:
        pass

    # Save changes to session
    if(session.session_key):
        Session.objects.save(session.session_key, session._session,
            datetime.datetime.now() + datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE))


        class RunFlashBlockNode(template.Node):
            def __init__(self, nodelist):
                self.nodelist = nodelist

    def render(self, context):

        session = context['request'].session
        ret = None
        if session.get('flash_msg', False):
            ret = {'msg': session['flash_msg']}
            if 'flash_params' in session:
                ret['params'] = session.get('flash_params', False)
            session_clear(session);

        if ret is not None:
            context.update(ret) 
            return self.nodelist.render(context)
        return ''


class RunFlashTemplateNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        session = context['request'].session
        if session.get('flash_msg', False):
            ret = {'msg': session['flash_msg']}
            if 'flash_params' in session:
                ret['params'] = session.get('flash_params', False)

            session_clear(session);
            try:
                template = settings.FLASH_TEMPLATE
            except AttributeError:
                template = 'elements/flash.html'
            return render_to_string(template, dictionary=ret) 
        return ''

def do_flash_template(parser, token):
    """
    Call template if there is flash message in session

    Runs a check if there is a flash message in the session.
    If the flash message exists it calls settings.FLASH_TEMPLATE
    and passes the template the variables 'msg' and 'params'.
    Calling this clears the flash from the session automatically

    To set a flash msg, in a view call:
    request.session['flash_msg'] = 'sometihng'
    request.session[flash_'params'] = {'note': 'remember me'}

    In the template {{ msg }} and {{ params.note }} are available
    """
    return RunFlashTemplateNode()

def do_flash_block(parser, token):
    """
    A block section where msg and params are both available.
    Calling this clears the flash from the session automatically

    If there is no flash msg, then nothing inside this block
    gets rendered

    Example:
    {% flash %}
        {{msg}}<br />
        {{params.somekey}}
    {% endflash %}
    """
    nodelist = parser.parse(('endflash',))
    parser.delete_first_token()
    return RunFlashBlockNode(nodelist)

register.tag('flash_template', do_flash_template)
register.tag('flash', do_flash_block)
