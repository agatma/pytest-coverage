from django.test import Client
from ..models import Post
from .set_up_tests import (
    PostTestSetUpMixin, PostPagesLocators, GroupLocators, PostLocators
)


class PostCreateFormTests(PostTestSetUpMixin):
    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTests.user)

    def test_posts_forms_create_post(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        form_data = {
            'text': PostLocators.TEXT_FOR_FORM,
            'group': GroupLocators.PK,
            'image': PostLocators.IMAGE_UPLOADED,
        }
        response = self.authorized_client.post(
            PostPagesLocators.POST_CREATE,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, PostPagesLocators.POST_PROFILE)
        self.assertEqual(Post.objects.count(), post_count + 1)

        self.assertTrue(
            Post.objects.filter(
                text=PostLocators.TEXT_FOR_FORM,
                group=PostCreateFormTests.group,
                image=f'posts/{PostLocators.GIF_FOR_TEST_NAME}',
            ).exists()
        )

    def test_posts_forms_edit_post(self):
        """Форма редактирует запись в Post."""
        tasks_count = Post.objects.count()
        form_data = {
            'text': PostLocators.EDIT_FORM_TEXT,
            'group': GroupLocators.PK,
        }
        response = self.authorized_client.post(
            PostPagesLocators.POST_EDIT,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, PostPagesLocators.POST_DETAIL)
        self.assertEqual(Post.objects.count(), tasks_count)
        response = self.authorized_client.get(PostPagesLocators.POST_DETAIL)
        text_post_object = response.context['page_obj'].text
        self.assertEqual(text_post_object, PostLocators.EDIT_FORM_TEXT)


# class CommentCreateFormTests(PostTestSetUpMixin):
#     def setUp(self):
#         self.authorized_client = Client()
#         self.authorized_client.force_login(PostCreateFormTests.user)
#
#     def test_posts_forms_create_post(self):
#         """Валидная форма создает комментарий к посту."""
#         post = Post.objects.get(pk=PostLocators.PK)
#         comments_count = post.comments.count()
#         form_data = {
#             'text': PostLocators.COMMENT_POST_TEXT_FORM,
#         }
#         response = self.authorized_client.post(
#             PostPagesLocators.ADD_COMMENT,
#             data=form_data,
#             follow=True
#         )
#         self.assertRedirects(response, PostPagesLocators.POST_DETAIL)
#         self.assertEqual(post.comments.count(), comments_count + 1)
#
#         self.assertTrue(
#             Post.objects.filter(
#                 text=PostLocators.TEXT_FOR_FORM,
#                 group=PostCreateFormTests.group,
#                 image=f'posts/{PostLocators.GIF_FOR_TEST_NAME}',
#             ).exists()
#         )
