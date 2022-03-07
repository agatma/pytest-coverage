# posts/tests/test_models.py
from django.conf import settings
from posts.tests.set_up_tests import PostLocators, PostTestSetUpMixin


class PostModelTest(PostTestSetUpMixin):
    def test_post_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post, group = PostModelTest.post, PostModelTest.group
        self.assertEqual(str(post), post.text[:settings.POST_SYMBOLS], )
        self.assertEqual(str(group), group.title, )

    def test_post_models_have_correct_verbose_names(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verbose = {
            'text': PostLocators.TEXT_VERBOSE,
            'pub_date': PostLocators.PUB_DATE_VERBOSE,
            'author': PostLocators.AUTHOR_VERBOSE_AND_HELP,
            'group': PostLocators.GROUP_VERBOSE,
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected
                )

    def test_post_models_have_correct_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_text = {
            'text': PostLocators.TEXT_HELP_TEXT,
            'pub_date': PostLocators.PUB_DATE_HELP_TEXT,
            'author': PostLocators.AUTHOR_VERBOSE_AND_HELP,
            'group': PostLocators.GROUP_HELP_TEXT,
        }
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                )
