from datetime import datetime
from django.views.generic.list_detail import object_detail, object_list
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from blog.models import Blog, Entry
from structure.models import Author
from tagging.models import Tag
from tagging.utils import calculate_cloud


def all_blogs(request, active=True):
    """
    List of all blogs. Defaults to listing active blogs.
    """
    blogs = Blog.objects.filter(active=active).order_by('order')
    featured = []
    for blog in blogs:
        featured.extend(Entry.objects.has_photos(blog)[:1])
    latest = Entry.objects.filter(pub_date__lte=datetime.now()).order_by('-pub_date')[:5]
    c = {
        'blogs': blogs,
        'active': active,
        #'archives': Blog.objects.filter(active=False).count() > 0,
        'featured': featured,
        'latest': latest,
    }
    return render(request, 'blog/blog_list.html', c)


def blog_index(request, blog, page=1):
    """
    Blog front page. Displays latest blog posts, excluding future posts.
    Paginated.
    """
    blog_tags = Tag.objects.usage_for_model(Entry, counts=True,
        filters=dict(blog__slug=blog))
    cloud = calculate_cloud(blog_tags)
    blog_obj = get_object_or_404(Blog, slug=blog)
    qs = Entry.objects.published_on_blog(blog).order_by('-pub_date')
    c = {'blog': blog_obj,
        'blog_tags': cloud}
    return object_list(request, queryset=qs, paginate_by=10, allow_empty=False,
        page=page, extra_context=c)


def blog_archive_month(request, blog, year, month, page=1):
    """
    Monthly archives. Displays all blog posts in a given month. Paginated.
    """
    year = int(year)
    month = int(month)
    qs = Entry.objects.get_month_on_blog(blog, year, month)
    if qs.count() > 0:
        c = {
            'blog': get_object_or_404(Blog, slug=blog),
            'month': datetime(year, month, 1)
        }
        if month == 1:
            c['prev_month'] = datetime(year - 1, 12, 1)
        else:
            c['prev_month'] = datetime(year, month - 1, 1)
        if month == 12:
            c['next_month'] = datetime(year + 1, 1, 1)
        else:
            c['next_month'] = datetime(year, month + 1, 1)
        return object_list(request, queryset=qs, paginate_by=10, allow_empty=False,
            extra_context=c, page=page)
    else:
        raise Http404


def blog_detail(request, blog, year, month, slug):
    """
    Entry detail. Displays a single full post, identified by its slug.
    """
    blog_obj = get_object_or_404(Blog, slug=blog)
    entry = get_object_or_404(Entry, slug=slug, blog=blog_obj)
    return render(request, 'blog/entry_detail.html', {
        'blog': blog_obj,
        'entry': entry,
        })


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
        if request.user.has_perm('blog.view_draft_entry') or (
            request.user.has_perm('blog.view_own_draft') and request.user ==
                entry.author.user):
            qs = Entry.objects.all()
            c = {'draft': True}
            if not entry.is_published:
                return object_detail(request, queryset=qs, object_id=post_id, extra_context=c)
            else:
                return HttpResponseRedirect(entry.get_absolute_url())
        else:
            raise Http404


def blog_all_authors(request, blog):
    """
    All author profiles for an individual blog on one page. Whee!
    """
    qs = Author.objects.select_related(depth=2).filter(entry__blog__slug__exact=blog)
    c = {'blog': get_object_or_404(Blog, slug=blog)}
    return object_list(request, queryset=qs, extra_context=c)
