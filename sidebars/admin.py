from django.contrib import admin
from sidebars.models import NewsCalendarItem, ArtsCalendarShowtime, ArtsCalendarItem, \
    TalkingHeadsAnswer, TalkingHeadsItem, EventType


class NewsCalendarItemAdmin(admin.ModelAdmin):
    list_display = ['name','start_time','location']
    list_filter  = ['start_time',]

admin.site.register(NewsCalendarItem, NewsCalendarItemAdmin)

class ArtsCalendarShowtimeInline(admin.TabularInline):
    model = ArtsCalendarShowtime

class ArtsCalendarItemAdmin(admin.ModelAdmin):
    '''
    fields = (
        ('Event Info', {'fields': ['name', 'location', 'event_type', 'description']}),
        ('Event Dates', {'fields': ['start_time', 'end_time']})
    )
    '''
    inlines = [
        ArtsCalendarShowtimeInline,
    ]
    list_display = ('name','start_time','end_time','location')
    list_filter  = ['start_time',]

admin.site.register(ArtsCalendarItem, ArtsCalendarItemAdmin)

class TalkingHeadsAnswerInline(admin.TabularInline):
    model = TalkingHeadsAnswer

class TalkingHeadsItemAdmin(admin.ModelAdmin):
    inlines = [
        TalkingHeadsAnswerInline,
        ]
    list_display        = ('question','issue')

admin.site.register(TalkingHeadsItem, TalkingHeadsItemAdmin)

class EventTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(EventType, EventTypeAdmin)
