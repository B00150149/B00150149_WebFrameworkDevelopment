from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, Task, Profile, Challenge, ChallengeReview, MoodRating

# Form for registering a new user with roles
class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('user', 'Standard User'),
        ('premium', 'Premium User'),
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
    is_collaborative = forms.BooleanField(
        required=False,
        label="Make this a collaborative project",
        help_text="Allow other users to contribute to this project"
    )
    
    collaborators = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Add collaborators"
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'wallpaper', 'is_collaborative', 'collaborators']
        widgets = {
            'wallpaper': forms.RadioSelect(attrs={'class': 'wallpaper-radio'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        is_premium = kwargs.pop('is_premium', False)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['collaborators'].queryset = User.objects.exclude(id=user.id)
        
        if not is_premium:
            self.fields.pop('is_collaborative', None)
            self.fields.pop('collaborators', None)

# Form for creating challenge as event organizer
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'age_category', 'start_date', 'end_date', 'wallpaper']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'wallpaper': forms.RadioSelect(attrs={'class': 'wallpaper-radio'}),
        }

# Form for creating a new task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description',  'due_date'] #'assigned_to',

# Form for creating challenge reviews
class ChallengeReviewForm(forms.ModelForm):
    class Meta:
        model = ChallengeReview
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class MoodRatingForm(forms.ModelForm):
    class Meta:
        model = MoodRating
        fields = ['rating', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Optional notes about your mood...'
            }),
        }

# Form for editing user information
class UserEditForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('user', 'Standard User'),
        ('premium', 'Premium User'),
        ('organizer', 'Event Organizer'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(), label="Select Role")

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        # Pop the user instance to get profile role
        user_instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if user_instance:
            try:
                profile = user_instance.profile
                self.fields['role'].initial = profile.role
            except:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if commit:
            user.save()
            # Update or create profile role
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.email = user.email
            profile.save()
        return user
