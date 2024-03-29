# tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm

class PostTestCase(TestCase):

    # signup processing component test
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    # post creating component test
    def test_post_creation(self):
        post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post.')
        self.assertEqual(post.author, self.user)

    # no error in post creating component
    def test_post_form_valid(self):
        form_data = {'title': 'Test Post', 'content': 'This is a test post.'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    # they are errors in post creating component
    def test_post_form_invalid(self):
        form_data = {'title': '', 'content': ''}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
