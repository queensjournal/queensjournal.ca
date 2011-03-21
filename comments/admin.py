from comments.models import Comment, FreeComment
from django.contrib import admin

class CommentAdmin(admin.ModelAdmin):
	fields = (
		(None, {'fields': ('content_type', 'object_id', 'site')}),
		('Content', {'fields': ('person_name', 'person_email', 'person_location', 'comment')}),
		('Meta', {'fields': ('submit_date', 'is_public', 'ip_address', 'approved')}),
	)
	list_display = ('person_name', 'person_email', 'submit_date', 'content_type', 'get_content_object')
	list_filter = ('submit_date',)
	date_hierarchy = 'submit_date'
	search_fields = ('comment', 'person_name', 'person_email')
	
admin.site.register(Comment, CommentAdmin)

class FreeCommentAdmin(admin.ModelAdmin):
	fields = (
		(None, {'fields': ('content_type', 'object_id', 'site')}),
		('Content', {'fields': ('person_name', 'person_email', 'person_location', 'comment')}),
		('Meta', {'fields': ('submit_date', 'is_public', 'ip_address', 'approved')}),
	)
	list_display = ('person_name', 'person_email', 'submit_date', 'content_type', 'get_content_object')
	list_filter = ('submit_date',)
	date_hierarchy = 'submit_date'
	search_fields = ('comment', 'person_name', 'person_email')
	
admin.site.register(FreeComment, FreeCommentAdmin)
