from django.contrib.auth.models import User
from django.db.models import Model, TextField, DateTimeField, ForeignKey, CASCADE

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Message(Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    sender = ForeignKey(User, on_delete=CASCADE, verbose_name='sender', related_name='message_from', db_index=True)
    recipient = ForeignKey(User, on_delete=CASCADE, verbose_name='recipient', related_name='message_to', db_index=True)
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False, db_index=True)
    body = TextField('body')

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
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.sender.username))
        print("user.id {}".format(self.recipient.username))

        async_to_sync(channel_layer.group_send)("{}".format(self.sender.username), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.username), notification)

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
