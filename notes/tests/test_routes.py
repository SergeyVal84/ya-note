from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from django.contrib.auth.models import User
import pdb
from django.contrib.auth import get_user_model

User = get_user_model()

class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.notes = Note.objects.create(title='Заголовок', text='Текст', slug='test', author=cls.author)

    def test_home_page(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)



    def test_detail_page(self):
        self.client.force_login(self.author)
        url = reverse('notes:detail', args=[self.notes.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK) 