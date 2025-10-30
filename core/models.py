from django.db import models
from django.conf import settings
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
)


class BaseModel(TimeStampedModel, ActivatorModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_%(class)s_set',
                                   on_delete=models.SET_NULL, null=True, blank=True)
    
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_%(class)s_set',
                                   on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if user and not self.pk and not self.created_by:
            self.created_by = user
        if user:
            self.updated_by = user
        super().save(*args, **kwargs)

