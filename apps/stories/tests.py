"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import datetime

from django.test import TestCase
from stories.models import Story

class StoryTestHelper(object):
    STORY_DEFAULTS = {
        'head': 'Queen\'s Journal Implements testing framework, finally.',
        'deck': "Editor-in-Chief says this will help detect issues earlier",
        'slug': "journal-implements-tests",
        'section': '',
    }

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

