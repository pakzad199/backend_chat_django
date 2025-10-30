from django.db import models
from core.models import BaseModel
from room.models import Room
from django.contrib.auth.models import User


class Message(BaseModel):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    edited = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-created']


class Attachment(BaseModel):
    message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/%Y/%m/%d')