from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse

from authapp.models import User
from mainapp.models import News


class TestMainPageSmoke(TestCase):
    
    def test_page_open(self):
        url = reverse("mainapp:home")
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class NewsTestCase(TestCase):
    def setUp(self) -> None:
        for i in range(10):
            News.objects.create(
                title=f'News{i}',
                preambule=f'Preambule{i}',
                body=f'Body{i}'
            )

        User.objects.create_superuser(username='django', password='geekbrains')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url, {'username': 'django', 'password': 'geekbrains'}
        )

    def test_open_page(self):
        url = reverse('mainapp:news')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_failed_open_add_by_anonim(self):
        url = reverse('mainapp:news_create')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)







