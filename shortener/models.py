from django.db import models
from django.urls import reverse_lazy
from common.util.utils import get_unique_slug_or_existing
from accounts.models import CustomUser

class Link(models.Model):
    long_link = models.URLField()
    slug = models.SlugField('Slug for short link', unique=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                  related_name='links', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def get_absolute_url(self):
        return reverse_lazy('redirect_somewhere', kwargs={'slug':self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = get_unique_slug_or_existing(self, length=7)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.long_link} - {self.slug}'

    class Meta:
        ordering = ('-created_at',)


class Transition(models.Model):
    link = models.ForeignKey(
        Link, on_delete=models.CASCADE, related_name='transitions')
    ip = models.GenericIPAddressField()

    link_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-link_dt',)

    def __str__(self):
        return f'{self.link.slug} - {self.ip}'
