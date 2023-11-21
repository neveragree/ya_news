from http import HTTPStatus
from pytest_django.asserts import assertRedirects, assertFormError
import pytest

from django.urls import reverse

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


@pytest.mark.django_db
def test_user_can_create_comment(
    news, author_client, author, form_data, news_id_for_args
):
    url = reverse('news:detail', args=news_id_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    news, client, form_data, news_id_for_args
):
    url = reverse('news:detail', args=news_id_for_args)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_no_bad_words(author_client, news, form_data, news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    bad_words_data = f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
    form_data['text'] = bad_words_data
    response = author_client.post(url, data=form_data)
    assertFormError(response, 'form', 'text', errors=(WARNING))
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
        author_client,
        form_data,
        comment,
        comment_id_for_args,
        news_id_for_args
):
    url = reverse('news:edit', args=comment_id_for_args)
    response = author_client.post(url, form_data)
    news_url = reverse('news:detail', args=news_id_for_args)
    expected_url = news_url + '#comments'
    assertRedirects(response, expected_url)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_other_user_cant_edit_comment(
        admin_client,
        form_data,
        comment,
        comment_id_for_args,
):
    url = reverse('news:edit', args=comment_id_for_args)
    response = admin_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    note_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == note_from_db.text


def test_author_can_delete_comment(
        author_client, comment_id_for_args, news_id_for_args
):
    url = reverse('news:delete', args=comment_id_for_args)
    response = author_client.post(url)
    news_url = reverse('news:detail', args=news_id_for_args)
    expected_url = news_url + '#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_comment(
        admin_client, comment_id_for_args, news_id_for_args
):
    url = reverse('news:delete', args=comment_id_for_args)
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
