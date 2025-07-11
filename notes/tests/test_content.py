from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='test',
            author=cls.author
        )

    def test_note_in_list(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        notes = response.context['object_list']
        self.assertIn(self.notes, notes)

    def test_notes_in_author_list(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        notes = response.context['object_list']
        for note in notes:
            self.assertEqual(note.author, self.author)

    def test_aythor_has_form(self):
        self.client.force_login(self.author)
        for name in (('notes:edit', [self.notes.slug]), ('notes:add', None)):
            with self.subTest(name=name):
                url = reverse(name[0], args=name[1])
                response = self.client.get(url)
                self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
