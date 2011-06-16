from datetime import datetime
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from django.views.generic.simple import direct_to_template
from blog.models import Blog, Entry
from structure.models import Author
from staff.blog_admin.forms import AjaxPreviewForm, ProfileForm

def has_blog_access(user, blog):
	"""
	Helper function designed to test if user has access to a particular blog.
	This can either be a blog administrator (who has access to all blogs) or
	a blog author (who only has access to blogs that have that user set
	as a blogger).
	"""
	## test for blog existence
	try:
		blog_obj = Blog.objects.get(slug__exact=blog)
	except:
		return False
	
	## blog admins always have access
	if user.has_perms(['blog.add_blog','blog.change_blog','blog.delete_blog']):
		return True
	## blog authors only have access to blogs to which they are assigned
	else:
		if author_set.all() in blog_obj.bloggers.all():
			return True
		else:
			return False

def all_blogs(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
	else:
		try:
			profile = Author.objects.get(user=request.user)
		except Author.DoesNotExist:
			return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
		## blog admins always have access
		if request.user.has_perms(['blog.add_blog','blog.change_blog','blog.delete_blog']):
			blogs = Blog.objects.all()
		else:
			blogs = author.blog_set.all()
		if blogs.count() == 0:
			raise Http404
		else:
			return render_to_response('staff/blog/blog_list.html',
									  {'blogs': blogs},
									  context_instance=RequestContext(request))
	
def dashboard(request, blog):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
	elif has_blog_access(request.user, blog):
		c = {'blog': Blog.objects.get(slug__exact=blog)}
		if request.user.has_perm('blog.add_entry'):
			c['add_entry'] = True
		return render_to_response('staff/blog/dashboard.html',
								  c,
								  context_instance=RequestContext(request))
	else:
		return render_to_response('staff/access_denied.html',
								  {'missing': 'edit',
								   'staffapp': 'this blog'},
								  context_instance=RequestContext(request))		   

def profile_edit(request, blog):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
	else:
		try:
			profile = Author.objects.get(user=request.user)
		except Author.DoesNotExist:
			return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
		c = {'profile': profile,
			 'add_entry': request.user.has_perm('blog.add_entry'),
			 'blog': Blog.objects.get(slug__exact=blog)}
		if request.POST:
			form = ProfileForm(request.POST, request.FILES)
			c['form'] = form
			if form.is_valid():
				# save associated User fields
				user_obj = profile.user
				user_obj.name = form.cleaned_data['name']
				user_obj.email = form.cleaned_data['email']
				# change user password if applicable
				if form.cleaned_data.get('password2'):
					user_obj.set_password(form.cleaned_data['password2'])
				# save User object
				user_obj.save()
				# save Author fields
				if form.cleaned_data.get('homepage'):
					profile.homepage = form.cleaned_data['homepage']
				if form.cleaned_data.get('bio'):
					profile.bio = form.cleaned_data['bio']
				# grab portrait photo if available
				if form.cleaned_data.get('portrait'):
					profile.portrait = form.cleaned_data['portrait'].filename
					profile.save_portrait_file(profile.get_portrait_filename(),form.cleaned_data['portrait'].content)
				# save Author object
				profile.save()
				# set flash
				request.session['flash_msg'] = 'Profile successfully edited.'
				request.session['flash_params'] = {'type': 'success',
												   'action': 'profile'}
				return render_to_response('staff/blog/profile_form.html',
										  c,
										  context_instance=RequestContext(request))
			else:
				return render_to_response('staff/blog/profile_form.html',
										  c,
										  context_instance=RequestContext(request))
		else:
			form = ProfileForm({'name': profile.name,
								'email': profile.user.email,
								'homepage': profile.homepage,
								'bio': profile.bio})
			c['form'] = form
			return render_to_response('staff/blog/profile_form.html',
									  c,
									  context_instance=RequestContext(request))

def entries_index(request, blog):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
	elif has_blog_access(request.user, blog):
		c = {'blog': Blog.objects.get(slug__exact=blog)}
		# search
		if request.GET.get("s", ""):
			query = request.GET.get("s", "")
			qs = Entry.objects.filter(blog__slug__exact=blog)
			for term in query.split(" "):
				qs = qs.filter(Q(title__icontains=term) | Q(content__icontains=term) | Q(categories__name__icontains=term) | Q(author__user__name__icontains=term))
			c['query'] = query
		# filter by status
		elif request.GET.get("status", ""):
			status = request.GET.get("status", "")
			# two options for status: 'published', 'draft'
			if status == 'published':
				qs = Entry.objects.filter(blog__slug__exact=blog, is_published=True)
			elif status == 'draft':
				qs = Entry.objects.filter(blog__slug__exact=blog, is_published=False)
			c['status'] = status
		# filter by author
		elif request.GET.get("author", ""):
			author = request.GET.get("author", "")
			qs = Entry.objects.filter(blog__slug__exact=blog, author__user__username__exact=author)
			try:
				c['author'] = Author.objects.get(user__username__exact=author)
			except ObjectDoesNotExist:
				c['author'] = ''
		# filter by date
		elif request.GET.get("date", ""):
			year, month = request.GET.get("date", "").split('-')
			qs = Entry.objects.get_month_on_blog(blog, year, month)
			c['date'] = datetime.strptime('%s %s' % (year, month), "%Y %m")
		# all objects
		else:
			qs = Entry.objects.filter(blog__slug__exact=blog)
		if request.user.has_perm('blog.add_entry'):
			c['add_entry'] = True
		if request.user.has_perm('blog.change_entry'):
			c['edit_all_entries'] = True
		elif request.user.has_perm('blog.change_own_entry'):
			c['edit_all_entries'] = False
			c['edit_own_entries'] = True
		if request.user.has_perm('blog.view_draft_entry'):
			c['view_all_drafts'] = True
		elif request.user.has_perm('blog.view_own_draft'):
			c['view_own_drafts'] = True
			c['view_all_drafts'] = False
		c['full_list'] = Entry.objects.all()
		c['dates_list'] = Entry.objects.dates('pub_date','month',order='DESC')
		c['author_list'] = Author.objects.select_related(depth=1).filter(user__is_staff=True).order_by('name')
		if request.session.get('flash_params') and (request.session['flash_params'].get('action') == 'add' or request.session['flash_params'].get('action') == 'edit') and Entry.objects.count() > 0:
			request.session['flash_params']['new'] = Entry.objects.order_by('-id')[0]
		return object_list(request, qs, extra_context=c, allow_empty=True, paginate_by=30, template_name='staff/blog/entry_list.html')
	else:
		return render_to_response('staff/access_denied.html',
								  {'missing': 'edit',
								   'staffapp': 'this blog'},
								  context_instance=RequestContext(request))		   

def entry_edit(request, blog, e_id):
	entry = get_object_or_404(Entry, pk=e_id, blog__slug__exact=blog)
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
	elif has_blog_access(request.user, blog) and request.user.has_perm('blog.change_entry') or (request.user.has_perm('blog.change_own_entry') and entry.author.user == request.user):
		c = {'edit_entry': True,
			 'moderate_entry': request.user.has_perm('blog.moderate_entry'),
			 'blog': Blog.objects.get(slug__exact=blog)}
		if request.POST:
			url = request.POST.get('url', '/staff/blogs/%s/list/' % blog)
			# intercept a draft delete request
			if request.POST.get('draft-delete') == '1' and not entry.is_published and (request.user.has_perm('blog.delete_entry') or (request.user.has_perm('blog.delete_own_draft') and entry.author.user == request.user)):
				entry.delete()
				request.session['flash_msg'] = 'Draft successfully deleted.'
				request.session['flash_params'] = {'type': 'success',
												   'action': 'delete'}
				return HttpResponseRedirect(url)
			else:
				request.session['flash_msg'] = 'Entry successfully edited.'
				request.session['flash_params'] = {'type': 'success',
												   'action': 'edit'}
		else:
			url = '/staff/blogs/%s/list/' % blog
		return update_object(request,
							 model=Entry,
							 extra_context=c,
							 object_id=e_id,
							 template_name='staff/blog/entry_form.html',
							 post_save_redirect=url)
	else:
		return render_to_response('staff/access_denied.html',
								  {'missing': 'edit',
								   'staffapp': 'this entry'},
								  context_instance=RequestContext(request))		   

def entry_add(request, blog):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
	elif has_blog_access(request.user, blog) and request.user.has_perm('blog.add_entry'):
		c = {'author': Author.objects.get(user__username=request.user.username),
			 'moderate_entry': request.user.has_perm('blog.moderate_entry'),
			 'blog': Blog.objects.get(slug__exact=blog)}
		if request.POST:
			request.session['flash_msg'] = 'Entry successfully added.'
			request.session['flash_params'] = {'type': 'success',
											   'action': 'add'}
		return create_object(request,
							 model=Entry,
							 extra_context=c,
							 template_name='staff/blog/entry_form.html',
							 post_save_redirect='/staff/blogs/%s/list/' % blog)
	else:
		return render_to_response('staff/access_denied.html',
								  {'missing': 'edit',
								   'staffapp': 'this entry'},
								  context_instance=RequestContext(request))		   

def entry_ajax_preview(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/staff/login/?return=%s' % request.get_full_path())
	elif request.POST:
		form = AjaxPreviewForm(request.POST)
		if form.is_valid():
			preview = {
				'blog': form.cleaned_data['blog'],
				'title': form.cleaned_data['title'],
				'author': Author.objects.get(pk=form.cleaned_data['author']),
				'content': form.cleaned_data['content'],
				'pub_date': datetime.now(),
				}
			return render_to_response('staff/blog/entry_preview.html',
									  {'object': preview,
									   'media_url': settings.MEDIA_URL})
		else:
			return render_to_response('staff/blog/entry_preview.html',
									  {'errors': form.errors})
	else:
		return render_to_response('staff/blog/entry_preview.html',
								  {'display_head': True})
