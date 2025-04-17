from django.test import TestCase
from django.contrib.auth.models import User
from .models import Project, Task, Todo, MoodRating, Challenge, ChallengeParticipant  # Import your models here

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.project = Project.objects.create(name="Test Project", description="A project for testing.", owner=self.user)

    def test_project_creation(self):
        print("Running test_project_creation...")
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.description, "A project for testing.")
        self.assertEqual(self.project.owner, self.user)  # Check owner
        print("Project creation test passed.")

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.project = Project.objects.create(name="Test Project", description="A project for testing.", owner=self.user)
        self.task = Task.objects.create(title="Test Task", project=self.project)

    def test_task_creation(self):
        print("Running test_task_creation...")
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.project, self.project)
        print("Task creation test passed.")

class ProjectViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.project = Project.objects.create(name="Test Project", description="A project for testing.", owner=self.user)

    def test_project_list_view(self):
        print("Running test_project_list_view...")
        self.client.login(username='testuser', password='testpass')  # Log in the user
        response = self.client.get('/projectList/')  # Updated URL
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leisureProjects/projectList.html')
        print("Project list view test passed.")

class TodoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.todo = Todo.objects.create(title="Test Todo", user=self.user)

    def test_todo_creation(self):
        print("Running test_todo_creation...")
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertFalse(self.todo.completed)  # Default should be False
        self.assertEqual(self.todo.user, self.user)  # Check user
        print("Todo creation test passed.")

class MoodRatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.project = Project.objects.create(name="Test Project", description="A project for testing.", owner=self.user)
        self.task = Task.objects.create(title="Test Task", project=self.project)
        self.mood_rating = MoodRating.objects.create(user=self.user, project=self.project, task=self.task, rating=5)

    def test_mood_rating_creation(self):
        print("Running test_mood_rating_creation...")
        self.assertEqual(self.mood_rating.rating, 5)
        self.assertEqual(self.mood_rating.user, self.user)
        self.assertEqual(self.mood_rating.project, self.project)
        self.assertEqual(self.mood_rating.task, self.task)
        print("Mood rating creation test passed.")

class ChallengeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.challenge = Challenge.objects.create(title="Test Challenge", description="A challenge for testing.", age_category="All", start_date="2023-01-01", end_date="2023-12-31")

    def test_challenge_creation(self):
        print("Running test_challenge_creation...")
        self.assertEqual(self.challenge.title, "Test Challenge")
        self.assertEqual(self.challenge.description, "A challenge for testing.")
        self.assertEqual(self.challenge.age_category, "All")
        print("Challenge creation test passed.")

class ChallengeParticipantTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')  # Create a user
        self.challenge = Challenge.objects.create(title="Test Challenge", description="A challenge for testing.", age_category="All", start_date="2023-01-01", end_date="2023-12-31")
        
    def test_user_join_challenge(self): 
        print("Running test_user_join_challenge...")
        self.assertEqual(self.challenge.participants.count(), 0)         # Making sure that challenge has 0 participants
        ChallengeParticipant.objects.create(challenge=self.challenge, user=self.user) # Creating a ChallengeParticipant instance so user can join challenge
        self.assertIn(self.user, [participant.user for participant in self.challenge.participants.all()])  # Check if user is in participants
        print("User join challenge test passed.")
