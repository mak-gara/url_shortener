from msilib.schema import CustomAction
from django.contrib import admin

from .models import CustomUser

admin.site.register(CustomUser)
