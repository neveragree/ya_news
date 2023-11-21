import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def news_list():
    today = datetime.today()
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News.objects.create(
            title='Заголовок',
            text='Текст новости',
            date=today - timedelta(days=index)
        )
        all_news.append(news)
    return all_news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        text='Текст комментария',
        author=author,
    )
    return comment


@pytest.fixture
def comment_list(author, news):
    comment_list = []
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        comment_list.append(comment)
    return comment_list


@pytest.fixture
def news_id_for_args(news):
    return news.pk,


@pytest.fixture
def comment_id_for_args(comment):
    return comment.pk,


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст комментария',
    }
