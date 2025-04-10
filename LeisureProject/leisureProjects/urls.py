from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  
    path('aboutUs/', views.aboutUs, name="aboutUs"),
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    #Projects
    path('createProject/', views.create_project, name="createProject"),
    path('projectList/', views.project_list, name="projectList"),
    #TaskList
    path('createTask/<int:project_id>/', views.create_task, name="createTask"),
    path('taskList/<int:project_id>/', views.task_list, name="taskList"),
    path('tasks/<int:task_id>/toggle/', views.toggle_task_completion, name="toggleTaskCompletion"),
    #challenge
    path('createChallenge/', views.create_challenge, name='createChallenge'),
    path('challengeList/', views.challenge_list, name='challengeList'),
    path('challengeTaskList/<int:challenge_id>/', views.challenge_taskList, name="challengeTaskList"),
    #url for review with challange_id
    path('challenge/<int:challenge_id>/review/', views.create_review, name='createReview'),
    #to create. delete, iscompleted and get user specific to do list
    path('create-todo/', views.create_todo, name="createTodo"),  
    path('todos/', views.get_todos, name='get_todos'),
    path('todos/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
    path('todos/<int:todo_id>/toggle/', views.toggle_todo_completion, name='toggle_todo'),
]
