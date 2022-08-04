from pathlib import Path
from django.db import models
from django.urls import reverse_lazy
from django.core.files import File
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
