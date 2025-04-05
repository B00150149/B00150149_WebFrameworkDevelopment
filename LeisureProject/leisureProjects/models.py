from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# User Roles
USER_ROLES = [
    ('solo', 'Solo Hobbyist'),
    ('team', 'Team Hobbyist'),
    ('organizer', 'Event Organizer'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    email = models.EmailField(blank=True)  # Optional to avoid conflicts
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()}) - {self.email}'

class Project(models.Model):
    WALLPAPER_CHOICES = [
        ('wallpaper1.jpg', 'Wallpaper 1'),
        ('wallpaper2.jpg', 'Wallpaper 2'), 
        ('wallpaper3.jpg', 'Wallpaper 3'),
        ('wallpaper4.jpg', 'Wallpaper 4'),
        ('wallpaper5.jpg', 'Wallpaper 5'),
        ('wallpaper6.jpg', 'Wallpaper 6'),
        ('wallpaper7.jpg', 'Wallpaper 6'),
        ('wallpaper8.jpg', 'Wallpaper 6'),
      
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    wallpaper = models.CharField(
        max_length=50,
        choices=WALLPAPER_CHOICES,
        default='wallpaper1.jpg'
    )

    def __str__(self):
        return f'Project: {self.name} (Owner: {self.owner.username})'
    
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Task: {self.title} (Assigned to: {self.assigned_to.username if self.assigned_to else "Unassigned"})'
    
class TimeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'TimeLog: {self.task.title} by {self.user.username} (From {self.start_time} to {self.end_time})'
