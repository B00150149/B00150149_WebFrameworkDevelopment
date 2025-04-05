from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, Task, Profile

# Form for registering a new user with roles
class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('solo', 'Solo Hobbyist'),
        ('team', 'Team Hobbyist'),
        ('organizer', 'Event Organizer'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(), label="Select Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']  # Role is added here

    # Overriding the save method to save the profile with the selected role
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create the user's profile with role and email
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                email=self.cleaned_data['email']
            )
        return user

# Form for creating a new project
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'wallpaper']
        widgets = {
            'wallpaper': forms.RadioSelect(attrs={'class': 'wallpaper-radio'}),
        }

# Form for creating a new task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to']
