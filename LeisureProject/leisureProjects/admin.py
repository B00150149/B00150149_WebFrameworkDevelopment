from django.contrib import admin
from .models import Profile, Project, Task, TimeLog, Challenge, Todo

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Challenge)
admin.site.register(TimeLog)
admin.site.register(Todo)
# Register your models here.
