import pytest
from http import HTTPStatus

from django.urls import reverse


@pytest.mark.parametrize(
    ('name', 'method'),
    (('notes:home', 'get'), ('users:login', 'get'), ('users:logout', 'post'), ('users:signup', 'get'))
)

def test_pages_availability_for_anonymous_user(client, name, method):
    url = reverse(name,)
    response = getattr(client,method)(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.parametrize(
    'name',
    ('notes:list', 'notes:add', 'notes:success')
)
def test_pages_availability_for_auth_user(not_author_client, name):
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK