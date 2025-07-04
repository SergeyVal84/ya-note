from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model

User = get_user_model()

class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.notes = Note.objects.create(title='Заголовок', text='Текст', slug='test', author=cls.author)

    def test_home_page(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_user(self):
        url =(
                ('notes:list', None),
                ('notes:success', None),
                ('notes:add', None),
                ('notes:edit', [self.notes.slug]),
                ('notes:delete', [self.notes.slug]),
            )
        for name, args in url:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)



    def test_detail_edit_delete_note(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:detail', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=[self.notes.slug])
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_list_add_success_note(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.OK),
        )
        
        for user, status in users_statuses:
            url = (
                'notes:add',
                'notes:list',
                'notes:success',
                'users:login',
                'users:signup'
            )
            self.client.force_login(user)
            for name in url:
                with self.subTest(user=user, name=name):
                    url = reverse(name)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_logout(self):
        url = reverse('users:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
