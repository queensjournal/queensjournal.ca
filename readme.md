# queensjournal.ca
**Portia 2.0 GIT**    
_March 20, 2011 - Present_

Hello Journal-er of the future, this is Tyler Ball, writing to you from 
the PAST, of Volume 138. These are some notes covering the changes I've
made to the Journal site. If you've made it this far I'll assume you
want to change something. Please do, you probably know more about this
stuff than I do.

If you have questions please email me at tyler@tylerball.net or consult my transition manual.

##CHANGES FROM PREVIOUS VERSION

* **Issue-based structure to Time-based structure.** This is the biggest ideological change in the site. In the old site, all stories belonged to an issue, so even "web updates" and breaking news needed to be either tacked onto the previous issue or put into a new "extra" issue.
	
	The site now loads in new stories to the front page based on date. This, together with a better search implementation, allows for efficient retrieval of information for most users. It's how all the other newspapers do it.
	
	In addition to this, there's an [**archive**](http://queensjournal.ca/archives/) page for flipping through old issues.
		
* **More images, everywhere!** The previous site had basically one implementation for photos. I wanted to make it easier to do different things depending on the story. Now, the first photo for every story gets full-width top billing and the other stories get stacked a few paragraphs down.
    
    There's also a [photos page](http://queensjournal.ca/photos) to show off the most recent photo galleries. I'll also eventually work in an "issue in photos" widget for issue_index pages.
    
* **Tags.** I wanted the site to have some sort of taxonomy, but maintaining and conforming to a set of categories is a lot of work. Tagging is flexible and each year's EIC(s) can use them how they see fit. There's also a tag bar for the most popular tags, which is a great way to drive traffic to topics you want to push to your readers.

* **Author Profiles.** Now every author on gets a paginated list of the stories they've written, along with a place for a little bio and their headshot.

    Blog Entries also used to have a separate User profile model. Now the blogs use the same Author model as stories do, for simplicity.
    
* **Videos.** There is now a videos app that uses django-oembed to easily embed videos from YouTube or Vimeo.

* **Disqus.** Comments are now implemented with Disqus. If you're here because you don't know how to moderate comments, email me and I'll get you a login. If Disqus ever goes up in smoke (knock on an entire forest) contact me and I will try to help move the comments to something new.

###TODO:
* Front Page standalone photo solution.
* Issue in Photos
* Incorporate photos to author pages, especially for photo staff
* Mobile site
* lift quotes
* better Issuu integration/workflow
* Queued story publishing/tweeting
* Add videos, galleries, authors, etc to the Search indexes

##DJANGO

The site runs on Django 1.3. The stable release at the time
of development.

##DEPENDENCIES

###Python packages:
These are readily available through the [Python Package Index](http://pypi.python.org/pypi) if you ever need to update them. I've
installed [pip](http://www.pip-installer.org/) on the server, so you'll be able to update these packages easily.

* [django-imagekit](https://github.com/jdriscoll/django-imagekit/): This powers all the photo resizing for the site. It requires the Python Image Library.

* [django-disqus](https://github.com/arthurk/django-disqus): I used this to export the old comments to disqus. It also easily generates the comment include code in templates.

* [django-tagging](http://code.google.com/p/django-tagging/): Provides the tagging infrastructure. Will probably move to django-taggit soon, as this project hasn't been updated in a few years.

* [django-haystack](http://haystacksearch.org/): For the Search. I'm using xapian as the backend, which is really easy to install on Webfaction using [these instructions](http://forum.webfaction.com/viewtopic.php?pid=14394#p14394)

* [typogrify](http://code.google.com/p/typogrify/) handles some typographic functions, like converting quotes into smart quotes and apostrophes.

* [django-shorturls](https://github.com/jacobian/django-shorturls) generates and redirects all the short urls on the site. It requires the following Apache redirect in the httpd.conf file:
    
        RewriteEngine on
        RewriteCond %{http_host} ^qjrnl.net [nc]
        RewriteRule ^(.*)$ http://www.queensjournal.ca/s$1 [r=301,nc]
    
* [django-oembed](http://code.google.com/p/django-oembed/) handles all the video embedding in the video app.

* [django-pagination](http://code.google.com/p/django-pagination/) is easy-as-pie pagination for querysets. I use it for the author pages.

* [south](http://south.aeracode.org/) is for database schema migrations.

###Javascript:
The site uses the following Javascript libraries, storied in the templates/static/js:

* [jQuery](http://jquery.com/), version 1.4.  
jQuery plugins:
    * [Nivo Slider](http://nivo.dev7studios.com/) for featured photo sliders.
    * [jQuery Masonry](http://masonry.desandro.com/) for lots of columny layout stuff like the front and section pages.
    
###CSS:
The site uses the [Blueprint CSS Framework](http://www.blueprintcss.org/) for css reset and basic layout.

-----------------------------------------------------------------------
**Portia 1.5 GIT**  
_January, 2011_

Minor design changes, which to be honest, didn't really improve anything.
The site was in this state from January-March 2011.

-----------------------------------------------------------------------
**Portia 1.1x SVN**  
_June 3, 2008_

This is a really quick and dirty README for keeping notes during development.
	
DJANGO VERSION
----
### JUNE 3 REVISION:
[A security fix](http://www.djangoproject.com/weblog/2008/may/14/security/) was added to the current Django install. The 0.96 bugfix was used as a template, as the trunk fix assumes the presence of auto-escaping, which landed on the Django trunk after 5819, and updating to the latest trunk would require 
modification of the site's templates.

Portia currently runs on Django 5819, which reincorporates FileField/ImageField models into newforms (required for the operation of the blog application). The app was originally built on the Django development branch, revision 4723 (just before the MySQL version split). As of revision 221 of the Portia code (July 12, 2007), the project ran on top of Django 5609 (the Unicode branch merge). The below patches may or may not be necessary; documentation is left intact just in case.

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

## SETTINGS
For comment moderation you will need to set AKISMET\_API\_KEY, found in  settings_local.py (you can see an example local settings file in the SVN package). You can get one at [wordpress.com](http://wordpress.com/) by signing up for an account; an API key will be e-mailed to you once the account registration process is complete. The Journal has an API key already; e-mail me for it if it ever gets lost, or just get a new key.

## DEPENDENCIES
All the dependencies listed below should be placed in a dependencies
directory inside the Journal project directory, and symbolic links
made as show below.

The gallery app uses the [jQuery Javascript framework](http://www.jquery.com) and the [Thickbox gallery script](http://jquery.com/demo/thickbox/). The Thickbox script requires some configuration, namely the location of the animated loading bar. Generally this should be in the same place as the Thickbox script itself.

The auto-adjusting image width feature in the individual story pages requires the use of the [django-template-utils package] (http://code.google.com/p/django-template-utils/). No symbolic link is necessary but the dependencies directory will require an \_\_init__.py file so Django will recognize it as an includable module.

The sanitize filter (which removes all but a template-specified subset of HTML tags from output) requires the use of [BeautifulSoup] (http://www.crummy.com/software/BeautifulSoup/), which must 
be installed somewhere on the PYTHONPATH.

Some templates rely on the use of the [Typogrify package] (http://code.google.com/p/typogrify/) for various HTML rendering 
niceties. Furthermore, Typogrify itself relies on [Smartypants] (http://web.chad.org/projects/smartypants.py/), which must be installed 
somewhere on the PYTHONPATH.

The comment moderation feature requires the use of the [django-comment-utils package](http://code.google.com/p/django-comment-utils/) and the [Akismet Python API](http://www.voidspace.org.uk/python/akismet_python.html). The comment-utils package also needs to be modified to utilize the "approved" field of FreeComment. Because of this requirement, comment-utils is now included in the Portia SVN proper and will be maintained as long as is necessary (basically we'll switch back to the vanilla package if James Bennett decides to add spam-to-trash-queue functionality to comment-utils).

##DEPLOYMENT
The following symbolic links need to be made (remember, ABSOLUTE PATHS, 
not relative paths):

    ln -s DJANGO\_ADMIN\_MEDIA\_DIR ADMIN\_MEDIA_DIR (standard Django link)
    ln -s JOURNAL\_PROJECT\_DIR/media/* MEDIA\_DIR/ (make the MEDIA_DIR before you do this)
    ln -s JOURNAL\_PROJECT\_DIR/media/js/admin ADMIN\_MEDIA_DIR/journal
    ln -s JOURNAL\_PROJECT\_DIR/dependencies/jquery/ MEDIA_DIR/js/
    ln -s JOURNAL\_PROJECT\_DIR/dependencies/thickbox/ MEDIA_DIR/js/

Also, you'll need to make a settings\_local.py (easiest way is to copy the template in the repository). MAKE SURE YOUR MEDIA\_URL HAS A TRAILING SLASH. I cannot stress this enough; if you don't have the trailing slash after the URL then urlparse.urljoin fucks with you every time you call the get\_FIELD_url() method on any FileField or ImageFIeld.
