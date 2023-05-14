from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from main.models import UserStory
from bs4 import BeautifulSoup


class IndexPageFormLoads(TestCase):
    def setUp(self):
        self.url = ''
        self.response = self.client.get(self.url)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def tearDown(self):
        pass

    def test_page_loads_successfully(self):
        """tests if the user stories page loads successfully"""
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        """tests if the correct template is used"""
        self.assertTemplateUsed(self.response, 'main/index.html')

    def test_form_elements_exist(self):
        """tests if the form fields are correctly loaded"""
        salary_input = self.soup.find('input', {'id': 'salary'})
        eventtype_select = self.soup.find('select', {'id': 'eventtype'})
        relationship_select = self.soup.find('select', {'id': 'relationship'})

        self.assertIsNotNone(salary_input)
        self.assertIsNotNone(eventtype_select)
        self.assertIsNotNone(relationship_select)

    def test_how_it_works_exist(self):
        """tests if the question mark and a
        how does it work button are correctly loaded"""
        button = self.soup.find('button', {'id': 'info-button'})
        popup = self.soup.find('div', {'id': 'info-popup'})

        self.assertIsNotNone(button)
        self.assertIsNotNone(popup)


class UserStoriesPageLoads(TestCase):

    def setUp(self):
        self.story1 = UserStory.objects.create(
            title="Test Story 1",
            content="This is a test story.",
            created_at=datetime(2021, 1, 1)
        )
        self.story2 = UserStory.objects.create(
            title="Test Story 2",
            content="This is another test story.",
            created_at=datetime(2021, 2, 1)
        )

        self.url = reverse('user_stories')
        self.response = self.client.get(self.url)

    def test_page_loads_successfully(self):
        """tests if the user stories page loads successfully"""
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        """tests if the correct template is used"""
        self.assertTemplateUsed(self.response, 'main/user_stories.html')

    def test_user_stories_displayed(self):
        """tests if the user stories are displayed on the page"""
        self.assertContains(self.response, 'Test Story 1')
        self.assertContains(self.response, 'This is a test story.')

        self.assertContains(self.response, 'Test Story 2')
        self.assertContains(self.response, 'This is another test story.')

    def test_no_user_stories(self):
        """tests if the "No user stories are available"
         message is displayed when there are no user stories
         """
        UserStory.objects.all().delete()

        response = self.client.get(self.url)
        self.assertContains(response, 'No user stories are available at the moment.')
