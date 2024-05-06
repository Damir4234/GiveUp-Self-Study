from django.contrib import admin

from user.models import User, CompletedTasks

admin.site.register(User)
admin.site.register(CompletedTasks)
