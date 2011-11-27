from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from polls.models import Poll, Choice, Vote
from polls.forms import PollVotingForm

def poll_cookie_debug(request):
    c = {'remote_addr': request.META.get('REMOTE_ADDR'),
        'sessionid': request.COOKIES.get(settings.SESSION_COOKIE_NAME)}
    return render_to_response('polls/debug.html',
        c,
        context_instance=RequestContext(request))


def poll_vote(request, poll):
    return_url = '/'
    if request.POST:
        form = PollVotingForm(poll, request.POST)
        if request.COOKIES.get(settings.SESSION_COOKIE_NAME) is None:
            return poll_error(request, poll, "This poll requires cookies. If you rejected the cookie we attempted to set, you will need to accept it before you can vote on polls.", close_form=False)
        else:
            # has this person voted already?
            # CHECK: has the session_hash already voted on this poll?
            if Vote.objects.filter(poll=poll,session_hash=request.COOKIES.get(settings.SESSION_COOKIE_NAME)).count() > 0:
                return poll_error(request, poll, "You've alread voted on this poll.", close_form=True)
            # CHECK: has the IP address already hit its vote limit of 10?
            elif Vote.objects.filter(poll=poll, ip_address=request.META.get('REMOTE_ADDR')).count() > 2:
                return poll_error(request, poll, "You cannot vote on this poll: too many votes from your IP.", close_form=True)
            # CHECK: has anyone voted within the last five seconds?
            # last-resort flood protection
            elif Vote.objects.filter(poll=poll, submit_date__gte=datetime.now()-timedelta(seconds=2)).count() > 0:
                return poll_error(request, poll, "Vote flood protection activated. Please try voting again in a couple of seconds.", close_form=False)

            # okay, vote is valid, check the form
            if form.is_valid():
                poll_obj = Poll.objects.get(pk=poll)
                request.session['vote'].append(poll_obj.id)
                request.session['planetary'] = request.session['vote']
                return_url = request.POST.get('url', '/')
                Vote.objects.create(choice=Choice.objects.get(pk=form.cleaned_data['choice']),
                                           poll=Poll.objects.get(pk=poll),
                                           ip_address=request.META.get('REMOTE_ADDR'),
                                           session_hash=request.COOKIES.get(settings.SESSION_COOKIE_NAME),
                                           submit_date=datetime.now())
                return HttpResponseRedirect(return_url)
            else:
                return poll_error(request, poll, "There was an error submitting your vote. Please try again.", close_form=False)
    else:
        return HttpResponseRedirect(return_url)


def poll_error(request, poll, message, close_form):
    poll_obj = Poll.objects.get(pk=poll)
    request.session['poll_id'] = poll_obj.id
    request.session['poll_msg'] = message
    request.session['poll_params'] = {'type': 'voteflood'}
    if request.session.get('vote', None) is not None and poll_obj.id not in request.session.get('vote') and close_form:
        request.session['vote'].append(poll_obj.id)
    return HttpResponseRedirect(request.get_full_path())
