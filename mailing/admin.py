from django.contrib import admin

from .models import Mail

@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'subscribed_at')
    list_display_links = ('email',)
