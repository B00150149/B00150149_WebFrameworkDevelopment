from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# User Roles
USER_ROLES = [
    ('user', 'Standard User'),
    ('premium', 'Premium User'),
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(User, related_name='collaborative_projects', blank=True)
    is_collaborative = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    wallpaper = models.CharField(
        max_length=50,
        choices=WALLPAPER_CHOICES,
        default='wallpaper1.jpg'
    )

    def __str__(self):
        return f'Project: {self.name} (Owner: {self.owner.username})'

#For user: Event Organizer
class Challenge(models.Model):
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
    title = models.CharField(max_length=200)
    description = models.TextField()
    age_category = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    wallpaper = models.CharField(
        max_length=50,
        choices=WALLPAPER_CHOICES,
        default='wallpaper1.jpg'
    )

    def __str__(self):
        return self.title
      
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    #assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Task: {self.title} (Assigned to: {self.assigned_to.username if self.assigned_to else "Unassigned"})'


class TimeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'TimeLog: {self.task.title} by {self.user.username} (From {self.start_time} to {self.end_time})'

class Todo(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Todo: {self.title} (User: {self.user.username})'

class ChallengeReview(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.challenge.title} ({self.rating}/5)'

class ChallengeParticipant(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} joined {self.challenge.title} on {self.join_date}'

class MoodRating(models.Model):
    RATING_CHOICES = [
        (1, 'Very Negative'),
        (2, 'Negative'),
        (3, 'Neutral'), 
        (4, 'Positive'),
        (5, 'Very Positive')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    session_reference = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        context = []
        if self.project:
            context.append(f"Project: {self.project.name}")
        if self.task:
            context.append(f"Task: {self.task.title}")
        return f'Mood: {self.get_rating_display()} by {self.user.username} at {self.timestamp} ({", ".join(context)})'
