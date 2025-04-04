from django.contrib import admin
from .models import Profile, Project, Task, TimeLog

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TimeLog)
# Register your models here.
