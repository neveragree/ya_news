import unittest

from django.test import TestCase

# Импортируем модель, чтобы работать с ней в тестах.
from news.models import News


@unittest.skip('Сохранен как пример')
# Создаём тестовый класс с произвольным названием, наследуем его от TestCase.
class TestNews(TestCase):
    TITLE = 'Заголовок новости'
    TEXT = 'Тестовый текст'

    # В методе класса setUpTestData создаём тестовые объекты.
    # Оборачиваем метод соответствующим декоратором.
    @classmethod
    def setUpTestData(cls):
        # Стандартным методом Django ORM create() создаём объект класса.
        # Присваиваем объект атрибуту класса: назовём его news.
        # При создании объекта обращаемся к константам класса через cls.
        cls.news = News.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
        )

    # Проверим, что объект действительно было создан.
    def test_successful_creation(self):
        # При помощи обычного ORM-метода посчитаем количество записей в базе.
        news_count = News.objects.count()
        # Сравним полученное число с единицей.
        self.assertEqual(news_count, 1)

    def test_title(self):
        # Сравним свойство объекта и ожидаемое значение.
        self.assertEqual(self.news.title, self.TITLE)