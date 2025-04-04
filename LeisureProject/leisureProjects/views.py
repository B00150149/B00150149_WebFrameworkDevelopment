from django.shortcuts import render, redirect
from .models import Project, Task
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
#Can only access when logged in
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, TaskForm,  RegisterForm



def index(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(owner=request.user)
    else:
        projects = Project.objects.none()  # Show no projects for anonymous users
    return render(request, 'leisureProjects/index.html', {'projects': projects})


def aboutUs(request):
    # About page doesn't need projects data
    return render(request, 'leisureProjects/aboutUs.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
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
    return redirect('login')

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'leisureProjects/projectList.html', {'projects': projects})

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('projectList')
    else:
        form = ProjectForm()
    return render(request, 'leisureProjects/createProject.html', {'form': form})

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
