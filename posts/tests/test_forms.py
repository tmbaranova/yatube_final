import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post

User = get_user_model()


class FormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_post(self):
        """Post create test"""
        post_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        post_data = {
            'text': 'Текст поста',
            'author': self.user,
            'image': uploaded,
        }
        response = FormsTests.authorized_client.post(reverse('posts:new_post'),
                                                     data=post_data,
                                                     follow=True)
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(Post.objects.filter(text='Текст поста',
                                            author=self.user,
                                            image='posts/small.gif').exists())

    def test_edit_post(self):
        """Post edit test"""
        FormsTests.test_post = Post.objects.create(text='Текст',
                                                   author=self.user)

        edit_post_data = {
            'text': 'Измененный текст',
            'author': FormsTests.user,
        }
        response = FormsTests.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={'username': FormsTests.user.username,
                            "post_id": FormsTests.test_post.id}),
            data=edit_post_data,
            follow=True)
        FormsTests.edited_post = get_object_or_404(Post.objects.filter(
            id=FormsTests.test_post.id))

        self.assertRedirects(response,
                             reverse('posts:post', kwargs={
                                 'username': FormsTests.user.username,
                                 'post_id': FormsTests.test_post.id}))
        self.assertEqual(FormsTests.edited_post.text, 'Измененный текст')
