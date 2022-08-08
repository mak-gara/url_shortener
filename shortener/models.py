import datetime
import json
from pathlib import Path
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone, dateformat

from common.util.utils import get_unique_slug_or_existing, generate_and_save_qrcode
from accounts.models import CustomUser

class Link(models.Model):
    long_link = models.URLField()
    slug = models.SlugField('Slug for short link', unique=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                  related_name='links', blank=True, null=True)
    qrcode = models.ImageField(upload_to='qrcodes', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def get_absolute_url(self):
        return reverse_lazy('shortener:redirect_somewhere', kwargs={'slug':self.slug})
    
    @classmethod
    def get_user_links(cls, request):
        return cls.objects.filter(user=request.user)
    
    def total_transitions(self):
        return self.transitions.count()
    
    def get_transitions_per_day(self, days=10):
        now = timezone.now()
        days = [now - datetime.timedelta(i) for i in range(days-1, -1, -1)]
        values = [self.transitions.filter(link_dt__date=day).count() for day in days]
        days = [dateformat.format(day, 'd.m') for day in days]
        return days, values
    
    def save(self, *args, **kwargs):
        self.slug = get_unique_slug_or_existing(self, length=7)
        path = Path.cwd() / 'media' / 'qrcodes' / f'{self.slug}.svg'
        generate_and_save_qrcode(f'http://127.0.0.1/{self.slug}', path)
        self.qrcode = f'qrcodes/{self.slug}.svg'
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
