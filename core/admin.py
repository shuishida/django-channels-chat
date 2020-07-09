from django.contrib.admin import ModelAdmin, site
from core.models import Message


class MessageAdmin(ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'sender__username', 'recipient__username')
    list_display = ('id', 'sender', 'recipient', 'timestamp', 'characters')
    list_display_links = ('id',)
    list_filter = ('sender', 'recipient')
    date_hierarchy = 'timestamp'


site.register(Message, MessageAdmin)
