from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Comment, Post

User = get_user_model()


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="author", email="author@example.com", password="SafeTestPass123!")
        cls.reader = User.objects.create_user(username="reader", email="reader@example.com", password="SafeTestPass123!")
        cls.post = Post.objects.create(
            title="Тестовый пост на Django", summary="Описание", body="Пример текста для поиска", author=cls.author,
            is_published=True,
        )
        cls.draft = Post.objects.create(title="Черновик", body="Не опубликовано", author=cls.author)

    def test_home_and_about(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("about")).status_code, 200)

    def test_post_slug_url(self):
        self.assertIn("testovyy", self.post.slug)
        self.assertEqual(self.client.get(self.post.get_absolute_url()).status_code, 200)
        self.assertContains(self.client.get(self.post.get_absolute_url()), 'rel="canonical"')

    def test_old_id_address_redirects(self):
        response = self.client.get(reverse("blog:legacy_post_detail", args=[self.post.pk]))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, self.post.get_absolute_url())

    def test_search_and_draft_is_hidden(self):
        response = self.client.get(reverse("blog:post_list"), {"q": "поиска"})
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, "Черновик")
        self.assertNotContains(self.client.get(reverse("blog:post_list")), "Черновик")

    def test_pagination_keeps_search(self):
        for i in range(12):
            Post.objects.create(title=f"Django пост номер {i}", body="Django пример", author=self.author, is_published=True)
        response = self.client.get(reverse("blog:post_list"), {"q": "Django", "page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertContains(response, "q=Django")
        self.assertEqual(self.client.get(reverse("blog:post_list"), {"page": 999}).context["page_obj"].number, 3)

    def test_non_author_cannot_edit(self):
        self.client.force_login(self.reader)
        self.assertEqual(self.client.get(self.post.get_edit_url()).status_code, 403)
        self.assertEqual(self.client.get(self.post.get_delete_url()).status_code, 403)

    def test_auth_required_for_post_creation(self):
        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_author_can_create_and_delete(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse("blog:post_create"), {
            "title": "Создано из формы", "summary": "Коротко", "body": "Новый текст", "is_published": "on"
        })
        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title="Создано из формы")
        self.assertEqual(post.author, self.author)
        self.assertEqual(self.client.get(post.get_delete_url()).status_code, 200)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        self.assertEqual(self.client.post(post.get_delete_url()).status_code, 302)
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_comment_and_count(self):
        self.client.force_login(self.reader)
        response = self.client.post(self.post.get_absolute_url(), {"text": "Первый комментарий"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.reader).exists())
        self.assertContains(self.client.get(self.post.get_absolute_url()), "Первый комментарий")

    def test_anonymous_cannot_comment(self):
        response = self.client.post(self.post.get_absolute_url(), {"text": "Гость"})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(text="Гость").exists())

    def test_unique_slug(self):
        second = Post.objects.create(title=self.post.title, body="Дубль", author=self.author, is_published=True)
        self.assertNotEqual(second.slug, self.post.slug)
        self.assertEqual(self.client.get(second.get_absolute_url()).status_code, 200)

    def test_unpublished_only_owner(self):
        self.assertEqual(self.client.get(self.draft.get_absolute_url()).status_code, 404)
        self.client.force_login(self.author)
        self.assertEqual(self.client.get(self.draft.get_absolute_url()).status_code, 200)
