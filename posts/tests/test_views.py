import datetime
import shutil

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Follow, Group, Post

User = get_user_model()


class ViewsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

        cls.test_group = Group.objects.create(
            title='Группа',
            slug='group',
            description='Описание',
        )

        cls.user = User.objects.create_user(username='123')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.test_post = Post.objects.create(
            text='Текст',
            pub_date=datetime.datetime.now(),
            author=cls.user,
            group=cls.test_group,
            image=uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def tearDown(self):
        cache.clear()

    def test_cache(self):
        """Test to check correct work of cache"""
        post_data = {
            'text': 'Проверка кэша',
            'author': self.user}
        response = ViewsPagesTests.authorized_client.get(
            reverse('posts:index')).content

        ViewsPagesTests.authorized_client.post(
            reverse('posts:new_post'),
            data=post_data,
            follow=True
        )
        response_cached = ViewsPagesTests.authorized_client.get(
            reverse('posts:index')).content
        self.assertEqual(response, response_cached)

        cache.clear()
        response_with_new_post = ViewsPagesTests.authorized_client.get(
            reverse('posts:index')).content
        self.assertNotEqual(response, response_with_new_post)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'index.html': reverse('posts:index'),
            'group.html': reverse('posts:group_posts',
                                  kwargs={'slug': 'group'}),
            'new.html': reverse('posts:new_post'),
            'author.html': reverse('about:author'),
            'tech.html': reverse('about:tech'),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = ViewsPagesTests.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Test context for index page (post where group is indicated)"""
        response = ViewsPagesTests.authorized_client.get(
            reverse('posts:index'))
        post_object = response.context['page'][0]
        post_author = post_object.author
        post_group = post_object.group
        post_text = post_object.text
        post_image = post_object.image
        self.assertEqual(post_author, ViewsPagesTests.test_post.author)
        self.assertEqual(post_group, ViewsPagesTests.test_post.group)
        self.assertEqual(post_text, ViewsPagesTests.test_post.text)
        self.assertEqual(post_image, ViewsPagesTests.test_post.image)

    def test_group_page_show_correct_context(self):
        """Test context for group page (post where group is indicated)"""
        response = ViewsPagesTests.authorized_client.get(reverse(
            'posts:group_posts', kwargs={'slug': 'group'}))

        group_object = response.context['group']
        self.assertEqual(group_object, ViewsPagesTests.test_group)

        post_object = response.context['page'][0]
        self.assertEqual(post_object, ViewsPagesTests.test_post)

    def test_new_page_show_correct_context(self):
        """Test context for new page"""
        response = ViewsPagesTests.authorized_client.get(
            reverse('posts:new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Test context for edit post page"""
        response = ViewsPagesTests.authorized_client.get(
            reverse('posts:post_edit', kwargs={'username': self.user.username,
                                               "post_id": self.test_post.id}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_profile_show_correct_context(self):
        """Test context for profile page"""
        response = ViewsPagesTests.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': ViewsPagesTests.user.username,
                            }))
        author = response.context['author']

        author_username = author.username
        self.assertEqual(author_username, ViewsPagesTests.user.username)

        post_object = response.context['page'][0]
        post_author = post_object.author
        post_group = post_object.group
        post_text = post_object.text
        post_image = post_object.image
        self.assertEqual(post_author, ViewsPagesTests.test_post.author)
        self.assertEqual(post_group, ViewsPagesTests.test_post.group)
        self.assertEqual(post_text, ViewsPagesTests.test_post.text)
        self.assertEqual(post_image, ViewsPagesTests.test_post.image)

        test_post_count = author.posts.count()
        self.assertEqual(test_post_count, 1)

    def test_post_correct_context(self):
        """Test context for post page"""
        response = ViewsPagesTests.authorized_client.get(
            reverse('posts:post', kwargs={
                'username': ViewsPagesTests.user.username,
                "post_id": ViewsPagesTests.test_post.id}))

        post_object = response.context['post']
        post_author = post_object.author
        post_group = post_object.group
        post_text = post_object.text
        post_image = post_object.image
        self.assertEqual(post_author, ViewsPagesTests.test_post.author)
        self.assertEqual(post_group, ViewsPagesTests.test_post.group)
        self.assertEqual(post_text, ViewsPagesTests.test_post.text)
        self.assertEqual(post_image, ViewsPagesTests.test_post.image)

        test_post_count = post_object.author.posts.count()
        self.assertEqual(test_post_count, 1)

    def test_group_post_in_another_group(self):
        """Test to check output post with group for this group only"""
        self.group_without_post = Group.objects.create(
            title='Пустая группа',
            slug='empty_group',
            description='Описание пустой группы',
        )

        response = ViewsPagesTests.authorized_client.get(
            reverse('posts:group_posts', kwargs={'slug': 'empty_group'}))
        post_object = response.context['page']
        self.assertFalse(post_object)


class FollowersTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.follower = User.objects.create_user(username='follower',
                                                password='123')
        cls.following = User.objects.create_user(username='following',
                                                 password='123')
        cls.not_follower = User.objects.create_user(username='not_follower',
                                                    password='123')

        cls.follow = Follow.objects.create(
            user=cls.follower, author=cls.following
        )

        cls.follower_client = Client()
        cls.follower_client.login(username='follower', password='123')

        cls.not_follower_client = Client()
        cls.not_follower_client.login(username='not_follower', password='123')

        cls.test_post = Post.objects.create(
            text='Текст',
            author=cls.following,
        )

    def test__unfollowing(self):
        follow_count_before_unfollowing = Follow.objects.all().count()
        FollowersTests.follower_client.get(
            reverse('posts:profile_unfollow',
                    kwargs={'username': 'following'}))
        follow_count_after_unfollowing = Follow.objects.all().count()

        self.assertEqual(follow_count_before_unfollowing - 1,
                         follow_count_after_unfollowing)

    def test_following(self):
        follow_count_before_following = Follow.objects.all().count()
        FollowersTests.not_follower_client.get(
            reverse('posts:profile_follow', kwargs={'username': 'following'}))
        follow_count_after_following = Follow.objects.all().count()

        self.assertEqual(follow_count_before_following + 1,
                         follow_count_after_following)

    def test_new_post_in_follows_index(self):
        """Test to check following author's post in follower's news"""
        post = FollowersTests.test_post
        response = FollowersTests.follower_client.get(
            reverse('posts:follow_index'))
        post_object = response.context['page']
        self.assertTrue(post, post_object)

    def test_new_post_not_in_not_follows_index(self):
        """Test to check author's post in not follower's news"""
        response = FollowersTests.not_follower_client.get(
            reverse('posts:follow_index'))
        post_object = response.context['page']
        self.assertFalse(post_object)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='123')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        for i in range(15):
            cls.i = Post.objects.create(
                text=f'Текст поста № {i}',
                author=cls.user,
            )

    def tearDown(self):
        cache.clear()

    def test_first_page_containse_ten_records(self):
        response = PaginatorViewsTest.authorized_client.get(
            reverse('posts:index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_five_records(self):
        response = PaginatorViewsTest.authorized_client.get(
            reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 5)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        User.objects.all().delete()
        Post.objects.all().delete()
