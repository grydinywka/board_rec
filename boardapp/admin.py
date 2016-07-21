from django.contrib import admin

from .models import Message, Genre, Notice

admin.site.register(Message)
admin.site.register(Genre)
admin.site.register(Notice)
