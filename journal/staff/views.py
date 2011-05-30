from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from staff.forms import LoginForm

def user_login(request):
    if request.method != "POST":
        form = LoginForm()
        return render_to_response('staff/login.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.GET.get('return','/staff/'))
                else:
                    return render_to_response('staff/login.html',
                                              {'form': form,
                                               'login_failed': "The login you used has been deactivated. Please use an active user's login."},
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('staff/login.html',
                                          {'form': form,
                                           'login_failed': "The user doesn't exist or the password you used is incorrect."},
                                          context_instance=RequestContext(request))
        else:
            return render_to_response('staff/login.html',
                                      {'form': form,
                                       'login_failed': "The login was malformed."},
                                      context_instance=RequestContext(request))
       
def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return render_to_response('staff/logout.html',
                              (),
                              context_instance=RequestContext(request))

def index(request):
    if request.user.is_authenticated():
        return render_to_response('staff/apps.html',
                                  (),
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/staff/login/')
