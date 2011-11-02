<!-- This file is formatted in Markdown. You can view a compiled version of it at http://github.com/tylerball/queensjournal.ca -->

# queensjournal.ca
**Picasso 2.0 GIT**
_March 20, 2011 - Present_

Hello Journal-er of the future, this is Tyler Ball, writing to you from
the PAST, of Volume 138. These are some notes covering the changes I've
made to the Journal site. If you've made it this far I'll assume you
want to change something. Please do, you probably know more about this
stuff than I do.

If you have questions please email me at tyler@tylerball.net or consult my transition manual.

## INSTALLATION

Do yourself a favour and use [virtualenv](http://www.virtualenv.org/en/latest/index.html) and
[virtualenvwrapper](http://www.doughellmann.com/articles/pythonmagazine/completely-different/2008-05-virtualenvwrapper/index.html). Make sure you have PostgreSQL installed and a fresh database ready.

mkvirtualenv journal
cd $VIRTUAL_ENV
git init
git remote add origin git@github.com:tylerball/queensjournal.ca.git
git pull origin master
pip install -r requirements/dev.txt
fab setup_local
cd apps
cp settings_local.py.ex settings_local.py

Open and edit settings\_local.py, filling in all the corresponding information.

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

* [django-shorturls](https://github.com/jacobian/django-shorturls) generates and redirects all the short urls on the site. It requires the following nginx redirect:

server {
    listen 80;
    server_name www.qjrnl.net qjrnl.net;
    rewrite ^(.*)$ http://www.queensjournal.ca/s$1 permanent;
}

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
