Portia 2.0 GIT (www.queensjournal.ca)
March 20, 2011

Hello Journal-er of the future, this is Tyler Ball, writing to you from 
the PAST, of Volume 138. These are some notes covering the changes I've
made to the Journal site. If you've made it this far I'll assume you
want to change something. Please do, you probably know more about this
stuff than I do.

If you have questions please email me at tyler@tylerball.net or consult
my transition manual.

CHANGES FROM PREVIOUS VERSION
=============================

* Issue-based structure to Time-based structure. This is the biggest ideological change in the site. In the old site, all stories belonged to an issue, so even "web updates" and breaking news needed to be either tacked onto the previous issue or put into a new "extra" issue.
	
    The site now loads in new stories to the front page based on date. This, together with a better search implementation, allows for efficient retrieval of information for most users. It's how all the other newspapers do it.
		
	- More images, everywhere! The previous site had basically one implementation
	for photos. I wanted to make it easier to do different things depending on
	the story.
		- 
	
	- Rich text editing
	
	- Article tags. I wanted the site to have some sort of taxonomy, but 
	maintaining and conforming to a set of categories is a lot of work and 
	ManyToManyFields are a pain in the ass so why bother? Tagging is worry-free
	and each year's EIC(s) can use them how they see fit.
	
	- Author Profiles
	
	- Comments now implemented with Disqus. If you're here because you
	don't know how to moderate comments, email me and I'll get you a login.
	If Disqus ever goes up in smoke (knock on an entire forest) contact me
	and I will try to help move the comments to something new.
	
	- 
	
DJANGO
======

The site runs on Django 1.3. The stable release at the time
of development. I'm not as well-versed as Wes Fok is in the Django
codebase, but I don't foresee any major security problems in the near
future with this site. I'll keep an eye on it.

Also, the Webfaction app it runs on is mod_wsgi instead of mod_python, as 
mod_python is no longer in development.

DEPENDENCIES
============

This list is now longer because of added functionality.

Python packages:
These are readily available through the Python Package Index
(http://pypi.python.org/pypi) if you ever need to update them. I've
installed pip on the server, so you'll be able to update these packages
easily.
	- django-imagekit: This powers all the photo resizing for the site.
	It requires the Python Image Library.
	- django-disqus: I used this to export the old comments to disqus
	- django-tagging: Provides the tagging infrastructure. 
	It needs django-tagging-autocomplete: https://github.com/agarzola/jQueryAutocompletePlugin
	
	- django-haystack: For the Search. I'm using xapian as the backend, which
	is really easy to install on Webfaction using these instructions:
	http://forum.webfaction.com/viewtopic.php?pid=14394#p14394
	This is somewhat of a pain in the ass to get set up, but it was worth having
	integrated search over the old Google site search.	

-----------------------------------------------------------------------
Portia 1.5 (www.queensjournal.ca)

Minor design changes, which to be honest, didn't really improve anything.
The site was in this state from January-March 2011.

NOTES FOR ORIGINAL SITE FOLLOW:
-----------------------------------------------------------------------
Portia 1.1x SVN (Journal website)
June 3, 2008

This is a really quick and dirty README for keeping notes during development.
	
DJANGO VERSION
JUNE 3 REVISION: A security fix 
(http://www.djangoproject.com/weblog/2008/may/14/security/) was added to 
the current Django install. The 0.96 bugfix was used as a template, as 
the trunk fix assumes the presence of auto-escaping, which landed on the 
Django trunk after 5819, and updating to the latest trunk would require 
modification of the site's templates.

Portia currently runs on Django 5819, which reincorporates 
FileField/ImageField models into newforms (required for the operation 
of the blog application). The app was originally built on the Django 
development branch, revision 4723 (just before the MySQL version split). 
As of revision 221 of the Portia code (July 12, 2007), the project ran 
on top of Django 5609 (the Unicode branch merge). The below patches may 
or may not be necessary; documentation is left intact just in case.

As of Alpha 2, the MySQL patch in Django ticket 1760 will also need to 
be applied. The patch will be required until the patch is merged with 
the trunk; by that point it might be worth considering moving to 
PostgreSQL or making sure the MySQL-Python module is up to date.

If Django is installed on a system with a Python 2.5.1 pre-release (as 
in any release between 2.5.0-final and 2.5.1-final), the 
2.5 fix in ticket 3519 will also be necessary. (3519 has been marked as 
invalid because technically this is a Python bug, not a Django bug.)

As of Portia revision 98 the firstof fix in ticket 4123 is required to 
ensure the default story labels appear properly.

SETTINGS
For comment moderation you will need to set AKISMET_API_KEY, found in 
settings_local.py (you can see an example local settings file in the SVN 
package). You can get one at http://wordpress.com/ by signing up for an 
account; an API key will be e-mailed to you once the account 
registration process is complete. The Journal has an API key already; 
e-mail me for it if it ever gets lost, or just get a new key.

DEPENDENCIES
All the dependencies listed below should be placed in a dependencies
directory inside the Journal project directory, and symbolic links
made as show below.

The gallery app uses the jQuery Javascript framework 
(http://www.jquery.com) and the Thickbox gallery script 
(http://jquery.com/demo/thickbox/). The Thickbox script requires
some configuration, namely the location of the animated loading bar.
Generally this should be in the same place as the Thickbox script
itself.

The auto-adjusting image width feature in the individual story pages
requires the use of the django-template-utils package 
(http://code.google.com/p/django-template-utils/). No symbolic link is 
necessary but the dependencies directory will require an __init__.py 
file so Django will recognize it as an includable module.

The sanitize filter (which removes all but a template-specified subset 
of HTML tags from output) requires the use of BeautifulSoup 
(http://www.crummy.com/software/BeautifulSoup/), which must 
be installed somewhere on the PYTHONPATH.

Some templates rely on the use of the Typogrify package 
(http://code.google.com/p/typogrify/) for various HTML rendering 
niceties. Furthermore, Typogrify itself relies on Smartypants 
(http://web.chad.org/projects/smartypants.py/), which must be installed 
somewhere on the PYTHONPATH.

The comment moderation feature requires the use of the 
django-comment-utils package 
(http://code.google.com/p/django-comment-utils/) and the Akismet Python 
API (http://www.voidspace.org.uk/python/akismet_python.html). 
The comment-utils package also needs to be modified to utilize the
"approved" field of FreeComment. Because of this requirement, 
comment-utils is now included in the Portia SVN proper and will be 
maintained as long as is necessary (basically we'll switch back to the 
vanilla package if James Bennett decides to add spam-to-trash-queue 
functionality to comment-utils).

DEPLOYMENT
The following symbolic links need to be made (remember, ABSOLUTE PATHS, 
not relative paths):
ln -s DJANGO_ADMIN_MEDIA_DIR ADMIN_MEDIA_DIR (standard Django link)
ln -s JOURNAL_PROJECT_DIR/media/* MEDIA_DIR/ (make the MEDIA_DIR before you do this)
ln -s JOURNAL_PROJECT_DIR/media/js/admin ADMIN_MEDIA_DIR/journal
ln -s JOURNAL_PROJECT_DIR/dependencies/jquery/ MEDIA_DIR/js/
ln -s JOURNAL_PROJECT_DIR/dependencies/thickbox/ MEDIA_DIR/js/

Also, you'll need to make a settings_local.py (easiest way is to copy the template in the repository). MAKE SURE YOUR MEDIA_URL HAS A TRAILING SLASH. I cannot stress this enough; if you don't have the trailing slash after the URL then urlparse.urljoin fucks with you every time you call the get_FIELD_url() method on any FileField or ImageFIeld.
