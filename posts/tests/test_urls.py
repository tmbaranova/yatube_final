from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_group = Group.objects.create(title='Название',
                                              slug='nazvanye')

        cls.user = User.objects.create_user(username='test_user')
        cls.not_author = User.objects.create_user(username='not_author',
                                                  password='123')

        cls.guest_client = Client()

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.not_author_client = Client()
        cls.not_author_client.login(username='not_author', password='123')

        cls.test_post = Post.objects.create(text='Текст', author=cls.user,
                                            group=cls.test_group)

    def tearDown(self):
        cache.clear()

    def test_urls_for_all_users(self):
        """Test urls allowed to all users"""
        url_names_for_all = [
            reverse('posts:index'),
            reverse('posts:group_posts',
                    kwargs={'slug': URLTests.test_group.slug}),
            reverse('posts:profile',
                    kwargs={'username': URLTests.user.username}),
            reverse('posts:post',
                    kwargs={'username': URLTests.user.username,
                            'post_id': URLTests.test_post.id}),
            reverse('about:author'),
            reverse('about:tech'),
        ]
        for url in url_names_for_all:
            with self.subTest(url=url):
                response = URLTests.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_urls_for_authorized_users(self):
        """Test urls allowed to authorized users only"""
        url_names_for_authorized = [
            reverse('posts:new_post'),
            reverse('posts:add_comment', kwargs={
                'username': URLTests.user.username,
                'post_id': URLTests.test_post.id}),
        ]
        for url in url_names_for_authorized:
            with self.subTest(url=url):
                response = URLTests.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_follow_and_unfollow_for_authorized_users(self):
        """Test urls for following and unfollowing allowed to authorized"""
        url_names_for_authorized = [
            reverse('posts:profile_follow', kwargs={
                'username': URLTests.user.username}),
            reverse('posts:profile_unfollow', kwargs={
                'username': URLTests.user.username}),
        ]
        for url in url_names_for_authorized:
            with self.subTest(url=url):
                response = URLTests.authorized_client.get(url)
                self.assertEqual(response.status_code, 302)

    def test_new_post_redirect_anonymous(self):
        url = reverse('posts:new_post')
        response = URLTests.guest_client.get(url, follow=True)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('posts:new_post')}")

    def test_comment_page_redirect_anonymous(self):
        kw = {'username': URLTests.test_post.author.username,
              'post_id': URLTests.test_post.id}
        url_name = reverse('posts:add_comment', kwargs=kw)

        response = URLTests.guest_client.get(url_name, follow=True)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next"
            f"={reverse('posts:add_comment', kwargs=kw)}")

    def test_follow_page_redirect_anonymous(self):
        kw = {'username': URLTests.user.username}
        url_names_for_authorized = reverse('posts:profile_follow',
                                           kwargs=kw)

        response = URLTests.guest_client.get(url_names_for_authorized,
                                             follow=True)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next="
            f"{reverse('posts:profile_follow', kwargs=kw)}")

    def test_unfollow_page_redirect_anonymous(self):
        kw = {'username': URLTests.user.username}
        url_names_for_authorized = reverse('posts:profile_unfollow',
                                           kwargs=kw)

        response = URLTests.guest_client.get(url_names_for_authorized,
                                             follow=True)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next="
            f"{reverse('posts:profile_unfollow', kwargs=kw)}")

    def test_redirect_edit_post_page_for_guest(self):
        kw = {'username': URLTests.test_post.author.username,
              'post_id': URLTests.test_post.id}
        url_name_for_author = reverse(
            'posts:post_edit', kwargs=kw)

        response = URLTests.guest_client.get(url_name_for_author, follow=True)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('posts:post_edit', kwargs=kw)}")

    def test_redirect_edit_post_page_for_authorized_but_not_author(self):
        kw = {'username': URLTests.test_post.author.username,
              'post_id': URLTests.test_post.id}
        url_name_for_author = reverse('posts:post_edit',
                                      kwargs=kw)

        response = URLTests.not_author_client.get(url_name_for_author,
                                                  follow=True)
        self.assertRedirects(
            response, f"{reverse ('posts:post', kwargs=kw)}")

    def test_edit_post_page_for_author(self):
        """Test url of edit post for post's author"""
        url_name_for_author = reverse('posts:post_edit',
                                      kwargs={
                                          'username': URLTests.user.username,
                                          'post_id': URLTests.test_post.id})

        response = URLTests.authorized_client.get(url_name_for_author)
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'index.html': reverse('posts:index'),
            'group.html': reverse('posts:group_posts',
                                  kwargs={'slug': URLTests.test_group.slug}),
            'new.html': reverse('posts:new_post'),
            'author.html': reverse('about:author'),
            'tech.html': reverse('about:tech'),
        }

        for template, reverse_name in templates_url_names.items():
            with self.subTest(template=template):
                response = URLTests.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_url_for_edit_page_uses_correct_template(self):
        templates_url_names = {
            'new.html': reverse('posts:post_edit',
                                kwargs={'username': URLTests.user.username,
                                        'post_id': URLTests.test_post.id})
        }

        for template, reverse_name in templates_url_names.items():
            with self.subTest(template=template):
                response = URLTests.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_page_not_found(self):
        url = reverse('posts:profile', kwargs={'username': 'not_found'})

        response = URLTests.authorized_client.get(url)
        self.assertEqual(response.status_code, 404)
