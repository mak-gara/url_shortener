from django.contrib import admin

from .models import Link, Transition


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'long_link', 'slug', 'user', 'created_at', 'updated_at')
    list_display_links = ('long_link', 'slug')
    
@admin.register(Transition)
class TransitionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ip', 'link', 'link_dt')
