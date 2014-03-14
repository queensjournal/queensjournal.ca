from django.template import RequestContext
from django.shortcuts import render_to_response


def server_error(request, template_name='500.html'):
    return render_to_response(template_name,
        context_instance=RequestContext(request))
