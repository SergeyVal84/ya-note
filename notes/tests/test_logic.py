from http import HTTPStatus
from pytils.translit import slugify
from django.test import TestCase, Client
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import pdb
from notes.forms import NoteForm

User = get_user_model()

class TestContentEditDelete(TestCase):

    NOTE_TEXT = 'Описание'
    NEW_NOTE_TEXT = 'Новое описание'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(title='Заголовок', text=cls.NOTE_TEXT, slug='slug_name', author=cls.author)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')
        cls.form_data = {'text': cls.NEW_NOTE_TEXT, 'title': 'Заголовок', 'author': 'author'}
        cls.list_url = reverse('notes:list')

    def test_edit_note(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)
    
    def test_not_author_cant_edit_note(self):
        response = self.not_author_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)

    
class TestContentAdd(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Пльзователь')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.success_url = reverse('notes:success')
        cls.form_data = {'text': 'Text', 'title': 'Заголовок', 'author': 'user'}
        cls.add_url = reverse('notes:add')

    def test_not_user_can_not__add_note(self):
        self.client.post(self.add_url, data=self.form_data)
        count_notes = Note.objects.count()
        self.assertEqual(count_notes, 0)
