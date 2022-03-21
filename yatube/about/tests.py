from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse

pages = ('/about/author/', '/about/tech/')
templates_url = {
    'about/author.html': '/about/author/',
    'about/tech.html': '/about/tech/'
}
reverse_url_names = ('about:author', 'about:tech')

templates_reverse_url = {
    'about/author.html': 'about:author',
    'about/tech.html': 'about:tech'
}


class AboutSetUpMixin(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.response_200 = HTTPStatus.OK


class AboutStaticURLTests(AboutSetUpMixin):
    def test_about_urls_exists_at_desired_location(self):
        """Проверка доступности адресов приложения about."""
        for url in pages:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
        self.assertEqual(response.status_code, self.response_200)

    def test_about_urls_uses_correct_template(self):
        """Проверка шаблонов для адресов приложения about."""
        for template, url in templates_url.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)


class AboutViewsTests(AboutSetUpMixin):
    def test_about_views_pages_accessible_by_name(self):
        """URL, генерируемый при помощи имени about:name, доступен."""
        for reverse_name in reverse_url_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse(reverse_name))
                self.assertEqual(response.status_code, self.response_200)

    def test_about_views_pages_use_correct_template(self):
        """При запросе к about:name
        применяется соответствующий шаблон."""
        for template, reverse_name in templates_reverse_url.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse(reverse_name))
                self.assertTemplateUsed(response, template)
