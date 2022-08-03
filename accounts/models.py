from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=False, db_index=True)
    
    class Meta(AbstractUser.Meta):
        pass
    
    def __str__(self):
        return self.username