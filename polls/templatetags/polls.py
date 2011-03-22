from django import template
from django.template import resolve_variable, Context
import datetime
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.conf import settings
from journal.polls.models import Poll
from journal.polls.forms import PollVotingForm

register = template.Library()

class PollFormNode(template.Node):
    def __init__(self, poll_id, var):
        self.poll_id, self.var = poll_id, var

    def render(self, context):
        poll = template.resolve_variable(self.poll_id, context)
        if Poll.objects.filter(pk=poll, close_date__gte=datetime.datetime.now()).count() > 0:
            context[self.var] = PollVotingForm(poll)
        return ''

def do_poll_form(parser, token):
    """
    {% poll_form poll_id as var %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, '%s takes two arguments' % bits[0]
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, 'Second argument of %s should be "as"' % bits[0]
    return PollFormNode(bits[1], bits[3])

register.tag('poll_form', do_poll_form)

def session_clear(session):
    """
    Private function, clear flash msgsfrom the session
    """
    try:
        del session['poll_id']
    except KeyError:
        pass

    try:
        del session['poll_msg']
    except KeyError:
        pass
    
    try:
        del session['poll_params']
    except KeyError:
        pass
    
    # Save changes to session
    if(session.session_key):
        Session.objects.save(session.session_key, session._session,
            datetime.datetime.now() + datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE))


class RunPollFlashBlockNode(template.Node):
    def __init__(self, nodelist, poll_id):
        self.nodelist, self.poll_id = nodelist, poll_id
        
    def render(self, context):
        poll = template.resolve_variable(self.poll_id, context)
        poll_obj = Poll.objects.get(pk=poll)
        session = context['request'].session
        if session.get('poll_id', False) == poll_obj.id:
            ret = None
            if session.get('poll_msg', False):
                ret = {'msg': session['poll_msg']}
                if 'poll_params' in session:
                    ret['params'] = session.get('poll_params', False)
                ret['poll'] = poll_obj.id
                session_clear(session);

            if ret is not None:
                context['pollmsg'] = ret
                return self.nodelist.render(context)
        return ''


def do_poll_flash_block(parser, token):
    """
    A block section where msg and params are both available.
    Calling this clears the flash from the session automatically
    
    If there is no flash msg, then nothing inside this block
    gets rendered
    
    Example:
    {% pollflash poll.id %}
        {{msg}}<br />
        {{params.somekey}}
    {% endpollflash %}
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError, "'%s' tag takes one argument" % bits[0]
    nodelist = parser.parse(('endpollflash',))
    parser.delete_first_token()
    return RunPollFlashBlockNode(nodelist, bits[1])

register.tag('pollflash', do_poll_flash_block)
