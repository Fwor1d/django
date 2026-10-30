from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


CYRILLIC = str.maketrans(dict(zip(
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
    ["a", "b", "v", "g", "d", "e", "yo", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya"]
)))


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
        null=True,
        blank=True,
    )
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField(
        "Адрес публикации", max_length=200, unique=True, blank=True,
        null=True, unique_for_date="created_at"
    )
    summary = models.CharField("Краткое описание", max_length=300, blank=True)
    body = models.TextField("Текст")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    is_published = models.BooleanField("Опубликовано", default=False)

    class Meta:
        ordering = ("-created_at", "-pk")
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title.lower().translate(CYRILLIC))[:175] or "post"
            candidate = base
            index = 2
            while type(self).objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                suffix = f"-{index}"
                candidate = base[:200 - len(suffix)] + suffix
                index += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def _url_parameters(self):
        if not self.created_at:
            raise ValueError("Публикацию нужно сохранить перед получением её URL")
        return {
            "year": timezone.localtime(self.created_at).year,
            "month": timezone.localtime(self.created_at).month,
            "day": timezone.localtime(self.created_at).day,
            "slug": self.slug,
        }

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs=self._url_parameters())

    def get_edit_url(self):
        return reverse("blog:post_edit", kwargs=self._url_parameters())

    def get_delete_url(self):
        return reverse("blog:post_delete", kwargs=self._url_parameters())


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField("Текст комментария")
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "-pk")
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий от {self.author} к {self.post}"
