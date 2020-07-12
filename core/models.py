from django.contrib.auth.models import User
from django.db.models import Model, TextField, DateTimeField, ForeignKey, CASCADE, CharField, ManyToManyField, SET_NULL

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class ChatGroup(Model):
    name = CharField(max_length=128, blank=True)
    members = ManyToManyField(User, related_name="chat_groups")

    def __str__(self):
        return self.name if self.name else " ".join([member.username for member in self.members.all()])


class Message(Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    sender = ForeignKey(User, on_delete=CASCADE, verbose_name='sender', related_name='+')
    group = ForeignKey(ChatGroup, on_delete=CASCADE, verbose_name='group', related_name='messages', db_index=True)
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False, db_index=True)
    body = TextField('body', max_length=4000)

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'receive_group_message',
            'message': f'{self.id}'
        }

        channel_layer = get_channel_layer()
        print("user.username {}".format(self.sender.username))

        members = self.group.members.all()
        for member in members:
            async_to_sync(channel_layer.group_send)(member.username, notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(Message, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = 'core'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
