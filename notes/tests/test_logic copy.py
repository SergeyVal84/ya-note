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

class TestLogic(TestCase):

    ADD_URL = reverse('notes:add')
    SUCCESS_URL = reverse('notes:success')
    # EDIT_URL = reverse('notes:edit', [self.notes.slug])
    # DELETE_URL = reverse('notes:delete', [self.notes.slug])
    TEXT_NOTE = 'Some text'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Автор')
        cls.author = Client()
        cls.author.force_login(cls.user)
        cls.reader = User.objects.create(username='Читатель')
        reader = Client()
        reader.force_login(cls.reader)
        cls.anonimus = Client()
        cls.author_1 = User.objects.create(username='Автор_1')
        # author_1 = Client()
        # author_1.force_login(cls.author_1)
        cls.author_2 = User.objects.create(username='Автор_2')
        # author_2 = Client()
        # author_2.force_login(cls.author_2)
        cls.note_1 = Note.objects.create(title='Заголовок', text='Текст', slug='test_1', author=cls.author_1)
        cls.note_2 = Note.objects.create(title='Заголовок', text='Текст', slug='test_2', author=cls.author_2)
        cls.form_data = {'title': 'Заголовок', 'text': 'Текст', 'slug':'test'}
        cls.form_data_author_1 = {'title': 'Заголовок', 'text': 'Текст', 'slug':'test',  'author': 'author_1'}
        cls.form_data_author_2 = {'title': 'Заголовок', 'text': 'Текст', 'slug':'test',  'author': 'author_2'}
        cls.form_data_no_slug = {'title': 'Заголовок', 'text': 'Текст', 'slug': None, 'author': cls.author}

    def test_delete_only_author(self):
        # self.author_1 = Client()
        # self.author_1.force_login(self.author_1)
        # self.author_1.force_login(self.user)
        response = self.author_1.post(reverse('notes:edit', kwargs={'slug': self.note_1.slug}), data={'title': 'Новый заголовок', 'text': 'Новый текст'})
        self.assertEqual(response.status_code, 200)




    def test_edit_only_author(self):
        ...


    def test_slug_is_none(self):
        response = self.client.post(self.ADD_URL, data=self.form_data)
        login_url = reverse('users:login')
        redirect_url = f'{login_url}?next={self.ADD_URL}'
        self.assertRedirects(response, redirect_url)
        if self.form_data_no_slug['slug'] is None:
            slug = slugify(self.form_data_no_slug['title'])
        self.author.force_login(self.user)
        form_data_no_slug = {'title': 'Заголовок', 'text': 'Текст', 'slug': slug, 'author': self.author}
        response = self.author.post(self.ADD_URL, data=form_data_no_slug)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 3)

    def test_add_note_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.ADD_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 3)

    def test_notuser_can_not_add_note(self):
        login_url = reverse('users:login')
        redirect_url = f'{login_url}?next={self.ADD_URL}'
        response = self.client.post(self.ADD_URL)
        self.assertRedirects(response, redirect_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 2)

    def test_slug_is_unique(self):
        all_notes = [
            Note(title='Заголовок', text='Текст', slug=f'test {index}', author=self.user)
            for index in range(2)
        ]
        Note.objects.bulk_create(all_notes)
        self.author.force_login(self.user)
        slug_1 = Note.objects.first().slug
        slug_2 = Note.objects.last().slug
        self.assertNotEqual(slug_1, slug_2)
