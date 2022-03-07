# posts/tests/test_urls.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Post, Group

User = get_user_model()


class UserLocators:
    USERNAME = 'auth'


class GroupLocators:
    TITLE = 'Тестовая группа'
    SLUG = 'new_test_group'
    DESCRIPTION = 'Тестовое описание'
    PK = 1


class PostLocators:
    TEXT = 'Тестовый пост'
    PK = '4242'
    TEXT_VERBOSE = 'Содержание поста'
    TEXT_HELP_TEXT = 'Введите текст поста'
    PUB_DATE_VERBOSE = 'Дата публикации поста'
    PUB_DATE_HELP_TEXT = 'Дата публикации поста (автоматически определяется)'
    AUTHOR_VERBOSE_AND_HELP = 'Автор поста'
    GROUP_VERBOSE = 'Название группы'
    GROUP_HELP_TEXT = 'Группа, к которой будет относиться пост'
    TEXT_FOR_FORM = 'Тестовый текст формы'
    EDIT_FORM_TEXT = 'Edit_new_text'


class PostPagesLocators:
    GUEST_PAGES = [
        '/', '/group/new_test_group/', '/profile/auth/', '/posts/4242/',
    ]
    PAGE_404 = '/test_404_page/'
    CREATE_EDIT_PAGES = ['/create/', '/posts/4242/edit/']
    POST_CREATE = reverse('posts:post_create')
    POST_PROFILE = reverse('posts:profile', kwargs={'username': 'auth'})
    POST_EDIT = reverse('posts:post_edit', kwargs={'post_id': '4242'})
    POST_DETAIL = reverse('posts:post_detail', kwargs={'post_id': '4242'})
    templates_url_names = [
        ('posts/index.html', '/'),
        ('posts/group_list.html', '/group/new_test_group/'),
        ('posts/profile.html', '/profile/auth/'),
        ('posts/post_detail.html', '/posts/4242/'),
        ('posts/create_post.html', '/create/'),
        ('posts/create_post.html', '/posts/4242/edit/'),
    ]
    templates = [
        ('posts/index.html', reverse('posts:index')),
        ('posts/group_list.html',
         reverse('posts:group_posts', kwargs={'slug': 'new_test_group'})),
        ('posts/profile.html',
         reverse('posts:profile', kwargs={'username': 'auth'})),
        ('posts/post_detail.html',
         reverse('posts:post_detail', kwargs={'post_id': '4242'})),
        ('posts/create_post.html', reverse('posts:post_create')),
        ('posts/create_post.html',
         reverse('posts:post_edit', kwargs={'post_id': '4242'})),
    ]
    templates_1_post = (
        reverse('posts:index'),
        reverse('posts:group_posts', kwargs={'slug': 'new_test_group'}),
        reverse('posts:profile', kwargs={'username': 'auth'}),
    )
    templates_context = (
        reverse('posts:index'),
        reverse('posts:group_posts', kwargs={'slug': 'new_test_group'}),
        reverse('posts:post_detail', kwargs={'post_id': '4242'}),
        reverse('posts:profile', kwargs={'username': 'auth'}),
    )
    templates_paginator = (
        reverse('posts:index'),
        reverse('posts:group_posts', kwargs={'slug': 'new_test_group'}),
        reverse('posts:profile', kwargs={'username': 'auth'}),
    )


class PostTestSetUpMixin(TestCase):
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
        cls.post = Post.objects.create(
            author=cls.user,
            text=PostLocators.TEXT,
            pk=PostLocators.PK,
            group=cls.group,
        )

    def check_url_response(self, pages, redirect=False, authorized=False):
        for url in pages:
            with self.subTest(url=url):
                if redirect:
                    response = self.guest_client.get(url, follow=True)
                    self.assertRedirects(response, f'/auth/login/?next={url}')
                elif authorized:
                    response = self.authorized_client.get(url)
                    self.assertEqual(response.status_code, self.response_200, )
                else:
                    response = self.guest_client.get(url)
                    self.assertEqual(response.status_code, self.response_200, )
