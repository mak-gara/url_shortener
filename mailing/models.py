from pyexpat import model
from django.db import models

class Mail(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ('-subscribed_at',)
