from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from django.views.generic.simple import direct_to_template
from django.contrib.contenttypes.models import ContentType
from stories.models import Story
from comments.models import FreeComment
from staff.commentmod.forms import SingleQuickActionForm

def comment_index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
    else:
        c = {}
        # search
        if request.GET.get("s", ""):
            query = request.GET.get("s", "")
            qs = FreeComment.objects.all()
            for term in query.split(" "):
                qs = qs.filter(Q(person_name__icontains=term) | Q(person_email__icontains=term) | Q(comment__icontains=term))
            c['query'] = query
        # filter by status
        elif request.GET.get("status", ""):
            status = request.GET.get("status", "")
            # three options for status: 'published', 'moderated', 'deleted'
            if status == 'published':
                qs = FreeComment.objects.filter(is_public=True)
            elif status == 'moderated':
                qs = FreeComment.objects.filter(is_public=False,approved=True)
            elif status == 'deleted':
                qs = FreeComment.objects.filter(is_public=False,approved=False)
            c['status'] = status
        # filter by parent object
        elif request.GET.get("ctype", "") and request.GET.get("objid", ""):
            content_type = request.GET.get("ctype", "")
            object_id = request.GET.get("objid", "")
            qs = FreeComment.objects.filter(content_type__id=content_type,object_id=object_id)
            try:
                c['parent'] = ContentType.objects.get(pk=content_type).get_object_for_this_type(pk=object_id)
            except ObjectDoesNotExist:
                c['parent'] = ''
        # all objects
        else:
            qs = FreeComment.objects.exclude(is_public=False,approved=False)
        if request.user.has_perm('comments.change_freecomment'):
            c['edit_comment'] = True
            c['approve_comment'] = True
            c['delete_comment'] = True
        c['full_list'] = FreeComment.objects.all()
        return object_list(request, qs, extra_context=c, allow_empty=True, paginate_by=30, template_name='staff/commentmod/comment_list.html')

def comment_edit(request, c_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
    elif request.user.has_perm('comments.change_freecomment'):
        c = {'edit_comment': True}
        child = FreeComment.objects.get(pk=c_id)
        try:
            c['parent'] = ContentType.objects.get(pk=child.content_type.id).get_object_for_this_type(pk=child.object_id)
        except:
            c['parent'] = ''
        if request.POST:
            request.session['flash_msg'] = 'Comment successfully edited.'
            request.session['flash_params'] = {'type': 'success'}
        return update_object(request,
                             model=FreeComment,
                             extra_context=c,
                             object_id=c_id,
                             template_name='staff/commentmod/comment_form.html',
                             post_save_redirect='/staff/comments/')
    else:
        return render_to_response('staff/access_denied.html',
                                  {'missing': 'edit',
                                   'staffapp': 'comments'},
                                  context_instance=RequestContext(request))        

def comment_quickaction(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
    elif request.user.has_perm('comments.change_freecomment') and request.POST:
        c = {'edit_comment': True}
        form = SingleQuickActionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            comment_id = form.cleaned_data['comment']
            redirect_url = form.cleaned_data['url']
            comment = FreeComment.objects.get(pk=comment_id)
            msg_success = False
            msg_failure = False
            if action == 'publish' and comment.is_public == False:
                comment.is_public = True
                comment.approved = True
                msg_success = 'Comment published.'
            elif action == 'moderate' and comment.is_public == True:
                comment.is_public = False
                comment.approved = True
                msg_success = 'Comment moved to moderation queue.'
            elif action == 'delete' and comment.approved == True:
                comment.is_public = False
                comment.approved = False
                msg_success = 'Comment deleted.'
            elif action == 'undelete' and comment.approved == False:
                comment.is_public = False
                comment.approved = True
                msg_success = 'Comment undeleted and moved to moderation queue.'
            else:
                msg_failure = 'No action taken. The action you tried to take was improper or has already been performed.'
            comment.save()
            if msg_success:
                request.session['flash_msg'] = msg_success
                request.session['flash_params'] = {'type': 'success'}
            elif msg_failure:
                request.session['flash_msg'] = msg_failure
                request.session['flash_params'] = {'type': 'failure'}
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponseBadRequest()
    else:
        return render_to_response('staff/access_denied.html',
                                  {'missing': 'edit',
                                   'staffapp': 'comments'},
                                  context_instance=RequestContext(request))        
