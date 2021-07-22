from django.http import HttpRequest
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse
from app.models import Question


class ViewTest(TestCase):

    def test_view_url_loads_properly(self):
        self.assertEqual(self.client.get(reverse('start')).status_code, 200)
        self.assertEqual(self.client.get(reverse('quiz')).status_code, 200)
        self.assertEqual(self.client.get(reverse('results')).status_code, 200)
        if self.assertEqual(self.client.get(reverse('create_question')).status_code, 302) is None:
            print('access to superuser link was denied')
        else:
            print('superuser check is not working')


class DatabaseTest(TestCase):

    def setUp(self) -> None:
        Question.objects.create(question_text='Test', right_answer=True)

    def test_database_working(self):
        question = Question.objects.first()
        self.assertEqual(question.question_text, 'Test')
        self.assertEqual(question.right_answer, True)
