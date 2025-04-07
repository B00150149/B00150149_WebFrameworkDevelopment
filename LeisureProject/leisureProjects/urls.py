from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Uncommented the index path
    path('createProject/', views.create_project, name="createProject"),
    path('aboutUs/', views.aboutUs, name="aboutUs"),
    path('createTask/<int:project_id>/', views.create_task, name="createTask"),
    path('projectList/', views.project_list, name="projectList"),
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('taskList/<int:project_id>/', views.task_list, name="taskList"),
    path('tasks/<int:task_id>/toggle/', views.toggle_task_completion, name="toggleTaskCompletion"),
]
