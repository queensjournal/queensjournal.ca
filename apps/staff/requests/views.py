from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from staff.requests.models import PhotoRequest
from structure.models import Author

def user_index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
    elif request.user.has_perm('requests.view_photorequest'):
        c = {}
        # search
        if request.GET.get("s", ""):
            query = request.GET.get("s", "")
            qs = PhotoRequest.objects.all()
            for term in query.split(" "):
                qs = qs.filter(Q(subject__icontains=term) | Q(location__icontains=term) | Q(notes__icontains=term))
            c['query'] = query
        # filter by status
        elif request.GET.get("status", ""):
            status = request.GET.get("status", "")
            qs = PhotoRequest.objects.filter(status=status)
            c['status'] = status
            c['status_display'] = qs[0].get_status_display()
        # filter by section
        elif request.GET.get("section", ""):
            section = request.GET.get("section", "")
            qs = PhotoRequest.objects.filter(section__slug=section)
            c['section'] = section
            c['section_display'] = qs[0].section.name
        # all objects
        else:
            qs = PhotoRequest.objects.all()
        if request.user.has_perm('requests.add_photorequest'):
            c['add_request'] = True
        if request.user.has_perm('requests.change_photorequest'):
            c['edit_request'] = True
        c['full_list'] = PhotoRequest.objects.all()
        return object_list(request, qs, extra_context=c, allow_empty=True, paginate_by=30, template_name='staff/requests/photorequest_list.html')
    else:
        return render_to_response('staff/access_denied.html',
                                  {'missing': 'view',
                                   'staffapp': 'photo requests'},
                                  context_instance=RequestContext(request))

def request_view(request, r_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
    elif request.user.has_perm('requests.view_photorequest'):
        qs = PhotoRequest.objects.all()
        pr = PhotoRequest.objects.get(id=r_id)
        try:
            au = Author.objects.get(user=pr.creator)
        except ObjectDoesNotExist:
            au = '%s %s' % (pr.creator.first_name, pr.creator.last_name)
        c = {'add_request': 'False',
            'author': au}
        if request.user.has_perm('requests.add_photorequest'):
            c['add_request'] = True
        return object_detail(request, queryset=qs, object_id=r_id, extra_context=c, template_name='staff/requests/photorequest_detail.html')
    else:
        return render_to_response('staff/access_denied.html',
                                  {'missing': 'view',
                                   'staffapp': 'photo requests'},
                                  context_instance=RequestContext(request))
    
def request_add(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
    elif request.user.has_perm('requests.add_photorequest'):
        c = {}
        if request.user.has_perm('requests.change_photorequest'):
            c['edit_request'] = True
        return create_object(request, PhotoRequest, extra_context=c, template_name='staff/requests/photorequest_form.html')
    else:
        return render_to_response('staff/access_denied.html',
                                  {'missing': 'add',
                                   'staffapp': 'photo requests'},
                                  context_instance=RequestContext(request))

def request_edit(request, r_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
    elif request.user.has_perm('requests.change_photorequest'):
        c = {'edit_request': True}
        return update_object(request, model=PhotoRequest, object_id=r_id, template_name='staff/requests/photorequest_form.html')
    else:
        return render_to_response('staff/access_denied.html',
                                  {'missing': 'edit',
                                   'staffapp': 'photo requests'},
                                  context_instance=RequestContext(request))
