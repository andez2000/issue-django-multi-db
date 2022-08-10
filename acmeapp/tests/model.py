from django.test import TestCase
from acmeapp.models import Post


class TestModels(TestCase):
    # doesnt fix it - cause Circular Dependency
    # databases = {'acmeapp_db'}
    # multi_db = False

    def setUp(self):
        Post.objects.create(title="This is a test")

    def test_Post_str(self):
        post = Post.objects.first()

        self.assertEqual(str(post), "This is a test")
