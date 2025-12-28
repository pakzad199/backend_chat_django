from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import User


class Room(BaseModel):
    name = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='rooms')
    
    def __str__(self):
        return self.name

