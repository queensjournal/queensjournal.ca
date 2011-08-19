# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 Arthur Furlan <arthur.furlan@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# On Debian systems, you can find the full text of the license in
# /usr/share/common-licenses/GPL-2

# I've made lots of customizations to this to get it to work with 
# django-shorturls and Journal apps, see below.
#        -Tyler

import os
import twitter
import urllib, urllib2
import urlparse # required for ShortURLS
from django.conf import settings
from django.contrib.sites.models import Site
from shorturls.templatetags.shorturl import ShortURL # ditto
from shorturls.baseconv import base62
from django.template.defaultfilters import striptags

TWITTER_MAXLENGTH = getattr(settings, 'TWITTER_MAXLENGTH', 140)

def post_to_twitter(sender, instance, *args, **kwargs):
        
    # Check if item is to be posted to Twitter. Make sure it's published.
    if instance.is_published is False:
        print 'Not published yet'
        return False

    # Check if model has been posted to Twitter:
    if instance.is_tweeted is False:
        instance.is_tweeted = True
        instance.save()
    else:
        return False
            
    # check if there's a twitter account configured
    try:
        consumer_key = settings.TWITTER_CONSUMER_KEY
        consumer_secret = settings.TWITTER_CONSUMER_SECRET
        access_token_key = settings.TWITTER_ACCESS_TOKEN_KEY
        access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
    except AttributeError:
        print 'WARNING: Twitter account not configured.'
        instance.is_tweeted = False
        return False

    # Set up SHORTURL
    baseurl = settings.SHORT_BASE_URL
    # grab ShortURL object for sender
    surl = ShortURL(instance)
    try:
        prefix = ShortURL.get_prefix(surl, instance)
    except (AttributeError, KeyError):
        print 'Error generating Prefix. Check settings.'
        instance.is_tweeted = False
        return False
        
    tinyid = base62.from_decimal(instance.pk)
    url = urlparse.urljoin(baseurl, prefix+tinyid)

    # create the twitter message
    try:
        text = striptags(instance.get_twitter_message())
    except AttributeError:
        text = unicode(instance)

    mesg = u'%s - %s' % (text, url)
    if len(mesg) > TWITTER_MAXLENGTH:
        size = len(mesg + '...') - TWITTER_MAXLENGTH
        mesg = u'%s... - %s' % (text[:-size], url)

    try:
        twitter_api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token_key, access_token_secret=access_token_secret)
        twitter_api.PostUpdate(mesg)
        print 'Posted to Twitter'
    except urllib2.HTTPError, ex:
        print 'ERROR:', str(ex)
        instance.is_tweeted = False
        return False
        