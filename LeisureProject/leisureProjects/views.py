from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

from .models import Project, Task, Todo, TimeLog
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Project, Task, Todo, ChallengeParticipant, MoodRating
from .forms import ProjectForm, TaskForm,  RegisterForm, ChallengeForm , MoodRatingForm, ChallengeReviewForm



def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_admin)
@require_POST
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if user_to_delete == request.user:
        messages.error(request, "You cannot delete yourself.")
    else:
        user_to_delete.delete()
        messages.success(request, f"User {user_to_delete.username} has been deleted.")
    return redirect('userList')


def index(request):
    from .models import ChallengeReview  # Import the ChallengeReview model

    if request.user.is_authenticated:
        projects = Project.objects.filter(owner=request.user)
        #to filter user specific list
        todos = Todo.objects.filter(user=request.user)   
    else:
        projects = Project.objects.none()
        todos = Todo.objects.none()
    return render(request, 'leisureProjects/index.html', {
        'projects': projects,
        'todos': todos
    })


def aboutUs(request):
    # About page doesn't need projects data
    return render(request, 'leisureProjects/aboutUs.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile for new user with default 'user' role
            from .models import Profile
            Profile.objects.create(user=user, role='user', email=user.email)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'leisureProjects/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('userList')
            else:
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'leisureProjects/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')




@login_required
def project_list(request):
    # Get both owned and collaborative projects
    owned_projects = Project.objects.filter(owner=request.user)
    collaborative_projects = Project.objects.filter(collaborators=request.user)
    is_premium = hasattr(request.user, 'profile') and request.user.profile.role == 'premium'
    return render(request, 'leisureProjects/projectList.html', {
        'owned_projects': owned_projects,
        'collaborative_projects': collaborative_projects,
        'is_premium': is_premium
    })

def create_project(request):
    is_premium = request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'premium'
    
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            if is_premium and 'is_collaborative' in request.POST:
                project.is_collaborative = True
            project.save()
            
            # Add collaborators if it's a collaborative project
            if project.is_collaborative and 'collaborators' in request.POST:
                collaborators = User.objects.filter(id__in=request.POST.getlist('collaborators'))
                project.collaborators.set(collaborators)
                
            return redirect('projectList')
    else:
        form = ProjectForm()
        users = User.objects.exclude(id=request.user.id) if is_premium else []
        
    return render(request, 'leisureProjects/createProject.html', {
        'form': form,
        'is_premium': is_premium,
        'users': users,
        'collaborate': request.GET.get('collaborate') == 'true'
    })

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def user_list(request):
    users = User.objects.select_related('profile').all()
    return render(request, 'leisureProjects/user_list.html', {'users': users})

@login_required
def delete_user(request, user_id):
    # Only allow admin to delete users
    if not request.user.is_superuser and not (request.user.username == 'admin' and request.user.email == 'admin@admin.com'):
        messages.error(request, "You do not have permission to delete users.")
        return redirect('userList')

    user_to_delete = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        if user_to_delete == request.user:
            messages.error(request, "You cannot delete yourself.")
            return redirect('userList')
        user_to_delete.delete()
        messages.success(request, f"User {user_to_delete.username} has been deleted.")
        return redirect('userList')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('userList')



###########################Tasks#########################################

import json
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from django.utils.timezone import make_aware
from datetime import timedelta

@login_required
def task_list(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'leisureProjects/taskList.html', {
        'project': project,
        'tasks': tasks,
        'now': timezone.now()
    })

@login_required
def task_progress_graph(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project)

    # Annotate each task with total time spent in seconds
    time_spent_expr = ExpressionWrapper(F('timelog__end_time') - F('timelog__start_time'), output_field=DurationField())
    tasks_with_time = tasks.annotate(total_time=Sum(time_spent_expr))

    task_labels = []
    time_data = []

    for task in tasks_with_time:
        task_labels.append(task.title)
        total_seconds = task.total_time.total_seconds() if task.total_time else 0
        hours = round(total_seconds / 3600, 2)
        time_data.append(hours)

    context = {
        'project': project,
        'task_labels': json.dumps(task_labels),
        'time_data': json.dumps(time_data),
    }
    return render(request, 'leisureProjects/taskProgressGraph.html', context)



from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def create_task(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('projectList')
    else:
        form = TaskForm()
    return render(request, 'leisureProjects/createTask.html', {'form': form, 'project': project})

@csrf_exempt
@require_POST
def toggle_task_completion(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'success': True, 'completed': task.completed})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)

@csrf_exempt
@require_POST
def log_time_spent(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
    try:
        data = json.loads(request.body)
        task_id = data.get('task_id')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')

        if not all([task_id, start_time_str, end_time_str]):
            return JsonResponse({'success': False, 'error': 'Missing parameters'}, status=400)

        task = Task.objects.get(id=task_id)
        start_time = timezone.datetime.fromisoformat(start_time_str)
        end_time = timezone.datetime.fromisoformat(end_time_str)

        # Ensure start_time and end_time are timezone aware
        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time, timezone.get_current_timezone())
        if timezone.is_naive(end_time):
            end_time = timezone.make_aware(end_time, timezone.get_current_timezone())

        TimeLog.objects.create(
            task=task,
            user=request.user,
            start_time=start_time,
            end_time=end_time
        )
        return JsonResponse({'success': True})
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


####################CHALLENGE###############################################################################################
@login_required
def create_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('challengeList') 
    else:
        form = ChallengeForm()
    return render(request, 'leisureProjects/createChallenge.html', {'form': form})

from .models import Challenge

def challenge_list(request):
    challenges = Challenge.objects.all().order_by('-start_date')
    return render(request, 'leisureProjects/challengeList.html', {'challenges': challenges})

def challenge_taskList(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    #only want admin to see review page code 
    if request.user.is_authenticated and request.user.username == "admin" and request.user.email == "admin@admin.com":
        reviews = challenge.reviews.all().order_by('-created_at')
    else:
        reviews = challenge.reviews.none()
    participants = challenge.participants.all()
    return render(request, 'leisureProjects/challengeTaskList.html', {
        'challenge': challenge,
        'reviews': reviews,
        'participants': participants,
        'now': timezone.now(),
        'is_participant': request.user.is_authenticated and 
                         challenge.participants.filter(user=request.user).exists()
    })

@login_required
def join_challenge(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    # Check if user already joined
    if not ChallengeParticipant.objects.filter(challenge=challenge, user=request.user).exists():
        ChallengeParticipant.objects.create(challenge=challenge, user=request.user)
    return redirect('challengeTaskList', challenge_id=challenge.id)

def create_review(request, challenge_id):
    challenge = Challenge.objects.get(id=challenge_id)
    if request.method == 'POST':
        form = ChallengeReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.challenge = challenge
            review.user = request.user
            review.save()
            return redirect('challengeTaskList', challenge_id=challenge.id)
    else:
        form = ChallengeReviewForm()
    return render(request, 'leisureProjects/createReview.html', {
        'form': form,
        'challenge': challenge
    })


####################to do list###############################################################################################
#Reference "https://www.geeksforgeeks.org/python-todo-webapp-using-django/"
@csrf_exempt
def create_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title and request.user.is_authenticated:
            todo = Todo.objects.create(
                title=title,
                user=request.user
            )
            return JsonResponse({'status': 'success', 'id': todo.id})
        return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@csrf_exempt
def get_todos(request):
    if request.user.is_authenticated:
        todos = Todo.objects.filter(user=request.user).values('id', 'title', 'completed')
        return JsonResponse({'todos': list(todos)})
    return JsonResponse({'todos': []})

@csrf_exempt
@require_POST
def delete_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)
        todo.delete()
        return JsonResponse({'status': 'success'})
    except Todo.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

@csrf_exempt
@require_POST
def toggle_todo_completion(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)
        todo.completed = not todo.completed
        todo.save()
        return JsonResponse({'status': 'success', 'completed': todo.completed})
    except Todo.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

@csrf_exempt
@require_POST
def submit_mood_rating(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)
    
    mood_rating = MoodRating()
    mood_rating.user = request.user
    mood_rating.rating = request.POST.get('rating')
    mood_rating.notes = request.POST.get('notes')
    mood_rating.session_reference = request.POST.get('session_reference')
    
    # Get project and task IDs if provided
    project_id = request.POST.get('project')
    task_id = request.POST.get('task')
    
    if project_id:
        mood_rating.project_id = project_id
    if task_id:
        mood_rating.task_id = task_id

    mood_rating.save()
    return JsonResponse({
        'status': 'success',
        'rating': mood_rating.rating,
        'timestamp': mood_rating.timestamp.isoformat()
    })
