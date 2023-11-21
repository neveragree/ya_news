import pytest

from django.conf import settings
from django.urls import reverse

LAZY_CLIENT = pytest.lazy_fixture('client')
LAZY_ADMIN = pytest.lazy_fixture('admin_client')


@pytest.mark.django_db
def test_news_on_main_number_and_order(
    news_list, client
):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_news_on_main_number_and_order(
    news, comment_list, client, news_id_for_args
):
    url = reverse('news:detail', args=news_id_for_args)
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, contain_form',
    (
        (LAZY_CLIENT, False),
        (LAZY_ADMIN, True),
    )
)
def test_pages_contains_form(
    parametrized_client, contain_form, news_id_for_args
):
    url = reverse('news:detail', args=news_id_for_args)
    response = parametrized_client.get(url)
    assert ('form' in response.context) is contain_form
