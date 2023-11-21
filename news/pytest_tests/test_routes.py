from http import HTTPStatus
import pytest

from django.urls import reverse
from pytest_django.asserts import assertRedirects

LAZY_NEWS = pytest.lazy_fixture('news_id_for_args')
LAZY_COMMENT = pytest.lazy_fixture('comment_id_for_args')
LAZY_ADMIN = pytest.lazy_fixture('admin_client')
LAZY_AUTHOR = pytest.lazy_fixture('author_client')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', LAZY_NEWS),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    ),
)
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (LAZY_ADMIN, HTTPStatus.NOT_FOUND),
        (LAZY_AUTHOR, HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, comment_id_for_args, expected_status
):
    url = reverse(name, args=comment_id_for_args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', LAZY_COMMENT),
        ('news:edit', LAZY_COMMENT),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
