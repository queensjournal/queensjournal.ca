from journal.structure.models import Section, Issue
from journal.sidebars.models import NewsCalendarItem, ArtsCalendarItem, TalkingHeadsItem, SportsCalendarItem, PreviousStories

# Link sidebars to sections here.
# Perhaps make this an admin item in the future?
# Tie to sections via Content-Type?
SIDEBAR_SECTIONS = {
    'news': (NewsCalendarItem.objects, 'sidebars/news_sidebar.html'),
    'opinions-editorials': (TalkingHeadsItem.objects, 'sidebars/heads_sidebar.html'),
    'opinions': (TalkingHeadsItem.objects, 'sidebars/heads_sidebar.html'),
    'arts-entertainment': (ArtsCalendarItem.objects, 'sidebars/arts_sidebar.html'),
    'sports': (SportsCalendarItem.objects, 'sidebars/sports_sidebar.html'),
    }
