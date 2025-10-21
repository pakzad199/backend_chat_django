from django.db import models
from core.abstract import BlameableModel
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
)
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Room(ActivatorModel, TimeStampedModel, BlameableModel, models.Model):
    name = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='rooms')

def __str__(self):
    return self.name


class Message(ActivatorModel, TimeStampedModel, BlameableModel, models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

class Meta:
    ordering = ['-created_at']


class Attachment(ActivatorModel, TimeStampedModel, BlameableModel, models.Model):
    message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/%Y/%m/%d')