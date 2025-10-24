from django.db import models
from core.middleware.CurrentUserMiddleware import get_current_user
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
)
from django.contrib.auth.models import User

# User = settings.AUTH_USER_MODEL

class BaseModel(TimeStampedModel, ActivatorModel):
    created_by = models.ForeignKey(User, related_name='created_%(class)s_set',
                                   on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_%(class)s_set',
                                   on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk and not self.created_by:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)


class Room(BaseModel):
    name = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='rooms')

def __str__(self):
    return self.name


class Message(BaseModel):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

class Meta:
    ordering = ['-created_at']


class Attachment(BaseModel):
    message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/%Y/%m/%d')