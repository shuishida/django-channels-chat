from django.contrib.admin import ModelAdmin, site
from django.contrib import admin

from core.models import Message, ChatGroup


class MessageAdmin(ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'sender__username', 'group__name')
    list_display = ('id', 'sender', 'group', 'body', 'timestamp', 'characters')
    list_display_links = ('id',)
    list_filter = ('sender', 'group')
    date_hierarchy = 'timestamp'


site.register(Message, MessageAdmin)
admin.site.register(ChatGroup)