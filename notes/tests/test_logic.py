from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import pdb
from notes.forms import NoteForm

User = get_user_model()

class TestLogic(TestCase):

    ADD_URL = reverse('notes:add')
    # EDIT_URL = reverse('notes:edit', [self.notes.slug])
    # DELETE_URL = reverse('notes:delete', [self.notes.slug])

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        # cls.notes = Note.objects.create(title='Заголовок', text='Текст', slug='test', author=cls.author)
        cls.form_data = {'title': 'Заголовок', 'text': 'Текст', 'slug':'test'}


    def test_add_note_user(self):
        self.client.force_login(self.author)
        response = self.client.post(self.ADD_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_notuser_can_not_add_note(self):
        login_url = reverse('users:login')
        redirect_url = f'{login_url}?next={self.ADD_URL}'
        response = self.client.post(self.ADD_URL)
        self.assertRedirects(response, redirect_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_slug_is_unique(self):
        all_notes = [
            Note(title='Заголовок', text='Текст', slug=f'test {index}', author=self.author)
            for index in range(2)
        ]
        Note.objects.bulk_create(all_notes)
        self.client.force_login(self.author)
        response_1 = self.client.post(self.ADD_URL, data=self.form_data)
        response_2 = self.client.post(self.ADD_URL, data=self.form_data)
        slug_1 = Note.objects.first().slug
        slug_2 = Note.objects.last().slug
        self.assertNotEqual(slug_1, slug_2)



