from http import HTTPStatus
from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

pages = ['/auth/login/', '/auth/signup/', '/auth/logout/']
templates_url = {
    'users/login.html': '/auth/login/',
    'users/signup.html': '/auth/signup/',
    'users/logged_out.html': '/auth/logout/',
}
reverse_url_names = ['users:login', 'users:signup', 'users:logout', ]

templates_reverse_url = {
    'users/login.html': 'users:login',
    'users/signup.html': 'users:signup',
    'users/logged_out.html': 'users:logout',
}

User = get_user_model()


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем тестового пользователя."""
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.response_200 = HTTPStatus.OK

    def test_users_url_available_for_guest_user(self):
        """Проверка доступности адресов приложения users."""
        for url in pages:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, self.response_200)

    def test_users_url_correct_template(self):
        """Проверка шаблонов для адресов приложения users."""
        for template, url in templates_url.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)


class UsersViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.response_200 = HTTPStatus.OK

    def test_users_views_accessible_by_name(self):

        """URL, генерируемый при помощи имени users:name, доступен."""
        for reverse_name in reverse_url_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse(reverse_name))
                self.assertEqual(response.status_code, self.response_200)

    def test_users_views_correct_template(self):
        """При запросе к users:name
        применяется соответствующий шаблон."""
        for template, reverse_name in templates_reverse_url.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse(reverse_name))
                self.assertTemplateUsed(response, template)

    def test_users_views_correct_context(self):
        """Шаблон users/sighup.html сформирован с правильным контекстом."""
        response = self.guest_client.get('/auth/signup/')
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'email': forms.fields.EmailField,
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
