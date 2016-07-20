from django.contrib import admin

from .models import Message, Genre
admin.site.register(Message)
admin.site.register(Genre)
