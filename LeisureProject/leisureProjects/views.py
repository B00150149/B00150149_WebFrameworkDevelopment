from django.shortcuts import render, redirect
from .models import Project, Task, Todo
#ChallengeTask
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#Can only access when logged in
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, TaskForm,  RegisterForm, ChallengeForm , MoodRatingForm, ChallengeReviewForm
from .models import ChallengeParticipant, MoodRating



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

from django.contrib.auth.models import User

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




###########################Tasks#########################################
from django.utils import timezone

@login_required
def task_list(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'leisureProjects/taskList.html', {
        'project': project,
        'tasks': tasks,
        'now': timezone.now()
    })



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
