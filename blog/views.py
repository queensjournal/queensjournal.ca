from datetime import datetime, timedelta
from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from blog.models import Blog, Entry, Category
from structure.models import Author

def all_blogs(request, active=True):
    """
    List of all blogs. Defaults to listing active blogs.
    """
    qs = Blog.objects.filter(active=active).order_by('title')
    c = {'active': active,
         'archives': Blog.objects.filter(active=False).count() > 0}
    return object_list(request, queryset=qs, extra_context=c)

def blog_index(request, blog, page=1):
    """
    Blog front page. Displays latest blog posts, excluding future posts.
    Paginated.
    """
    blog_obj = get_object_or_404(Blog, slug=blog)
    qs = Entry.objects.published_on_blog(blog).order_by('-date_published')
    c = {'blog': blog_obj}
    return object_list(request, queryset=qs, paginate_by=10, allow_empty=False, page=page, extra_context=c)

def blog_archive_month(request, blog, year, month, page=1):
    """
    Monthly archives. Displays all blog posts in a given month. Paginated.
    """
    year = int(year)
    month = int(month)
    qs = Entry.objects.get_month_on_blog(blog, year, month)
    if qs.count() > 0:
        c = {'blog': Blog.objects.get(slug=blog),
             'month': datetime(year,month,1)}
        if month == 1:
            c['prev_month'] = datetime(year-1,12,1)
        else:
            c['prev_month'] = datetime(year,month-1,1)
        if month == 12:
            c['next_month'] = datetime(year+1,1,1)
        else:
            c['next_month'] = datetime(year,month+1,1)
        return object_list(request, queryset=qs, paginate_by=10, allow_empty=False, extra_context=c, page=page)
    else:
        raise Http404

def blog_detail(request, blog, year, month, slug):
    """
    Entry detail. Displays a single full post, identified by its slug.
    """
    year = int(year)
    month = int(month)
    c = {'blog': Blog.objects.get(slug=blog)}
    qs = Entry.objects.get_month_on_blog(blog, year,month)
    return object_detail(request, queryset=qs, slug_field='slug', slug=slug, extra_context=c)

def blog_draft_detail(request, post_id):
    """
    Draft entry detail. Displays a draft entry if the user is logged in and has
    the correct permissions.
    """
    if not request.user.is_authenticated():
        # pretend nothing's here, raise a 404
        raise Http404
    else:
        # test for object's existence
        entry = get_object_or_404(Entry, pk=post_id)
        if request.user.has_perm('blog.view_draft_entry') or (request.user.has_perm('blog.view_own_draft') and request.user == entry.author.user):
            qs = Entry.objects.all()
            c = {'draft': True}
            if not entry.is_published:
                return object_detail(request, queryset=qs, object_id=post_id, extra_context=c)
            else:
                return HttpResponseRedirect(entry.get_absolute_url())
        else:
            raise Http404
        
def blog_archive_author(request, blog, author_id, page=1):
    """
    Author archives. Displays all blog posts for a given author. Paginated.
    """
    author = get_object_or_404(Author, pk=author_id)
    qs = Entry.objects.get_author_on_blog(blog, author_id)
    if qs.count() > 0:
        c = {'blog': Blog.objects.get(slug=blog),
             'author': author}
        return object_list(request, queryset=qs, paginate_by=10, allow_empty=False, extra_context=c, page=page)
    else:
        raise Http404

def blog_archive_category(request, blog, cat_slug, page=1):
    """
    Category archives. Displays all blog posts for a given category. Paginated.
    """
    category = get_object_or_404(Category, slug__exact=cat_slug)
    qs = category.entry_set.published_on_blog(blog)
    if qs.count() > 0:
        c = {'blog': Blog.objects.get(slug=blog),
             'category': category}
        return object_list(request, queryset=qs, paginate_by=10, allow_empty=False, extra_context=c, page=page)
    else:
        raise Http404

def blog_search(request, blog):
    query = request.GET.get('s', '')
    qs = Entry.objects.published_on_blog(blog).select_related(depth=1)
    for term in query.split( ):
        qs = qs.filter(Q(title__icontains=term) | Q(content__icontains=term))
    c = {'blog': Blog.objects.get(slug=blog),
         'query': query}
    return object_list(request, queryset=qs, paginate_by=10, allow_empty=True, extra_context=c)
            
def blog_author(request, author_id):
    """
    Author profile. Displays the profile of the selected author.
    """
    qs = Author.objects.all()
    entries = Entry.objects.published().filter(author__id=author_id).order_by('-date_published')[:10]
    return object_detail(request, queryset=qs, object_id=author_id, extra_context={'entries': entries})

def blog_all_authors(request, blog):
    """
    All author profiles for an individual blog on one page. Whee!
    """
    qs = Author.objects.select_related(depth=2).filter(entry__blog__slug__exact=blog)
    c = {'blog': Blog.objects.get(slug=blog)}
    return object_list(request, queryset=qs, extra_context=c)

