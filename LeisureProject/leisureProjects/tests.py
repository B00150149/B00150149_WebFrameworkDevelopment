from django.test import TestCase
from django.contrib.auth.models import User
from .models import Project, Task  # Import your models here

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.project = Project.objects.create(name="Test Project", description="A project for testing.", owner=self.user)

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.description, "A project for testing.")
        self.assertEqual(self.project.owner, self.user)  # Check owner

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.project = Project.objects.create(name="Test Project", description="A project for testing.", owner=self.user)
        self.task = Task.objects.create(title="Test Task", project=self.project)

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.project, self.project)

class ProjectViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.project = Project.objects.create(name="Test Project", description="A project for testing.", owner=self.user)

    def test_project_list_view(self):
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.get('/projectList/')  # Updated URL
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leisureProjects/projectList.html')

# Add more tests as needed
