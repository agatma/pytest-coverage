from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from ..models import Post, Group
from .set_up_tests import (
    PostTestSetUpMixin, PostPagesLocators, PostLocators,
    UserLocators, GroupLocators
)

User = get_user_model()


class PostPagesTests(PostTestSetUpMixin):
    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_views_pages_uses_correct_templates(self):
        """URL-адрес всех страниц в views использует соответствующий шаблон
        Страницы: все страницы приложения posts."""
        for template, reverse_name in PostPagesLocators.templates:
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_views_pages_index_group_profile_post_numbers_1(self):
        """Проверяем, что на страницах есть 1 пост
        Страницы: 'posts:index', 'posts:group_posts', 'posts:profile'."""
        for reverse_name in PostPagesLocators.templates_1_post:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), 1)

    def test_post_views_post_create_show_correct_context(self):
        """Шаблон posts_create.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(PostPagesLocators.POST_CREATE)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_views_post_edit_initial_value(self):
        """Предустановленное значение формы."""
        response = self.authorized_client.get(PostPagesLocators.POST_EDIT)
        text_initial = response.context['form'].initial['text']
        self.assertEqual(text_initial, 'Тестовый пост')

    def test_post_views_pages_index_group_profile_show_correct_context(self):
        """Проверяем контекст поста на страницах. Страницы: 'posts:index',
        'posts:group_posts', 'posts:profile', 'posts:detail'."""
        for reverse_name in PostPagesLocators.templates_context:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                if reverse_name == PostPagesLocators.POST_DETAIL:
                    first_object = response.context['page_obj']
                else:
                    first_object = response.context['page_obj'][0]
                self.assertEqual(first_object.text, PostLocators.TEXT)
                self.assertEqual(
                    first_object.author.username, UserLocators.USERNAME
                )
                self.assertEqual(first_object.pk, int(PostLocators.PK))
                self.assertEqual(
                    first_object.group.title, GroupLocators.TITLE
                )
                self.assertEqual(first_object.text, PostLocators.TEXT)
                self.assertEqual(first_object.image, f'posts/{PostLocators.GIF_FOR_TEST_NAME_VIEWS}', )

    def test_post_index_cache_check(self):
        initial_response = self.authorized_client.get(PostPagesLocators.POST_INDEX).content
        Post.objects.get(pk=PostLocators.PK).delete()
        cache_response = self.authorized_client.get(PostPagesLocators.POST_INDEX).content
        self.assertEqual(
            initial_response,
            cache_response
        )
        cache.clear()
        response_after_clear_cashe = self.authorized_client.get(PostPagesLocators.POST_INDEX).content
        self.assertNotEqual(
            initial_response,
            response_after_clear_cashe,
        )


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем тестового пользователя, группу и пост."""
        super().setUpClass()
        cls.user = User.objects.create_user(username=UserLocators.USERNAME)
        cls.group = Group.objects.create(
            title=GroupLocators.TITLE,
            slug=GroupLocators.SLUG,
            description=GroupLocators.DESCRIPTION,
        )
        for _ in range(13):
            cls.post = Post.objects.create(
                author=cls.user,
                text=PostLocators.TEXT,
                group=cls.group,
            )

    def test_post_views_first_page_contains_ten_records(self):
        """Проверяем paginator на страницах. Страница: 'posts:index',
        'posts:group_posts', 'posts:profile', 'posts:detail'."""
        for reverse_name in PostPagesLocators.templates_paginator:
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_post_views_second_page_contains_three_records(self):
        for reverse_name in PostPagesLocators.templates_paginator:
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)


class CommentTests(PostTestSetUpMixin):
    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_comment_availability(self):
        """Проверяем отображение комментария для любого пользователя
        Комментарий создан в set_up_tests"""
        response = self.guest_client.get(PostPagesLocators.POST_DETAIL)
        text_initial = response.context['comments'][0]
        self.assertEqual(str(text_initial), PostLocators.COMMENT_POST_TEXT)


