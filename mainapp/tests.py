from http import HTTPStatus
from telnetlib import EC

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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
from config import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


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


# selenium


class TestNewsSelenium(StaticLiveServerTestCase):

    def setUp(self):
        for i in range(1, 5):
            User.objects.create_superuser(
                username=f'Random{i}',
                email=f'Email{i}',
                age=i,
                avatar=f'Avatar{i}'
            )
        for i in range(10):
            News.objects.create(
                title=f'News{i}',
                preambule=f'Preambule{i}',
                body=f'Body{i}'
            )
        User.objects.create_superuser(username='admin', password='geekbrains')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url, {'username': 'admin', 'password': 'geekbrains'}
        )
        super().setUp()
        self.selenium = WebDriver(
            executable_path=settings.SELENIUM_DRIVER_PATH_FF
        )
        self.selenium.implicitly_wait(10)
        # Login
        self.selenium.get(f"{self.live_server_url}{reverse('authapp:login')}")
        button_enter = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[type="submit"]')
            )
        )
        self.selenium.find_element_by_name("username").send_keys("admin")
        self.selenium.find_element_by_name("password").send_keys("geekbrains")
        button_enter.click()
        # Wait for footer
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "mt-auto"))
        )

    def test_create_button_clickable(self):

        path_list = f"{self.live_server_url}{reverse('mainapp:news')}"
        path_add = reverse("mainapp:news_create")

        self.selenium.get(path_list)
        button_create = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f'[href="{path_add}"]')
            )
        )
        print("Trying to click button ...")
        button_create.click()  # Test that button clickable
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.ID, "id_title"))
        )
        print("Button clickable!")

    # With no element - test will be failed
    # WebDriverWait(self.selenium, 5).until(
    # EC.visibility_of_element_located((By.ID, "id_title111"))
    # )
    def test_pick_color(self):

        path = f"{self.live_server_url}{reverse('mainapp:home')}"
        self.selenium.get(path)
        navbar_el = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "navbar"))
        )
        try:
            self.assertEqual(
                navbar_el.value_of_css_property("background-color"),
                "rgb(255, 255, 155)",
            )
        except AssertionError:
            with open(
                    "var/screenshots/001_navbar_el_scrnsht.png", "wb"
            ) as outf:
                outf.write(navbar_el.screenshot_as_png)
        raise

    def tearDown(self):

        # Close browser
        self.selenium.quit()
        super().tearDown()
