from http import HTTPStatus
from django.test.utils import override_settings
from authapp import models
from django.core import mail as email
from django.test import TestCase, Client
from django.urls import reverse
from mainapp import tasks
from mainapp.models import News
from authapp.models import User
from mainapp.models import Courses


# pages_tests
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

    def test_open_page_detail(self):
        news_obj = models.News.objects.first()
        url = reverse('mainapp:news_detail', args=[news_obj.pk])
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_failed_open_add_by_anonim(self):
        url = reverse('mainapp:news_create')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_page_open_news_crete_by_admin(self):
        path = reverse("mainapp:news_create")
        result = self.client_with_auth.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_create_in_web(self):
        counter_before = models.News.objects.count()
        path = reverse("mainapp:news_create")
        self.client_with_auth.post(
            path,
            data={
                "title": "NewTestNews001",
                "preambule": "NewTestNews001",
                "body": "NewTestNews001",
            },
        )

        self.assertGreater(models.News.objects.count(), counter_before)

    def test_page_open_update_deny_access(self):
        news_obj = models.News.objects.first()
        url = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_update_in_web(self):
        new_title = "NewTestTitle001"
        news_obj = models.News.objects.first()
        self.assertNotEqual(news_obj.title, new_title)
        path = reverse("mainapp:news_update", args=[news_obj.pk])
        result = self.client_with_auth.post(
            path,
            data={
                "title": new_title,
                "preambule": news_obj.preambule,
                "body": news_obj.body,
            },
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_delete_in_web(self):
        news_obj = models.News.objects.first()
        path = reverse("mainapp:news_delete", args=[news_obj.pk])
        self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


#  email_test

class TestTaskMailSend(TestCase):

    def test_mail_send(self):
        for i in range(1, 5):
            User.objects.create_superuser(
                username=f'Random{i}',
                email=f'Email{i}',
                age=i,
                avatar=f'Avatar{i}'
            )

        message_body = "test_message_text"
        user_obj = models.User.objects.first()
        tasks.send_feedback_to_email(message_body, user_obj.pk)
        self.assertEqual(email.outbox[0].body, message_body)


# cashes_page_testing

class CoursesDetailTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        for i in range(0, 5):
            Courses.objects.create(
                name=f'name {i}',
                description=f'description {i}',
                cost=i
            )
        self.client = Client()

    @override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache', }})
    def test_page_course_detail_open(self):
        course_obj = Courses.objects.first()
        url = reverse("mainapp:courses_detail", args=[course_obj.pk])
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)
