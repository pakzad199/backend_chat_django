from django.db import models
from django.contrib.auth.models import User
from core.middleware.CurrentUserMiddleware import get_current_user

class BlameableModel(models.Model):
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