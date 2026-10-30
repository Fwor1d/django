from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                ("slug", models.SlugField(blank=True, max_length=200, null=True, unique=True, unique_for_date="created_at", verbose_name="Адрес публикации")),
                ("summary", models.CharField(blank=True, max_length=300, verbose_name="Краткое описание")),
                ("body", models.TextField(verbose_name="Текст")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                ("is_published", models.BooleanField(default=False, verbose_name="Опубликовано")),
                ("author", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="posts", to=settings.AUTH_USER_MODEL, verbose_name="Автор")),
            ],
            options={"verbose_name": "Публикация", "verbose_name_plural": "Публикации", "ordering": ("-created_at", "-pk")},
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(verbose_name="Текст комментария")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to=settings.AUTH_USER_MODEL, verbose_name="Автор")),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="blog.post", verbose_name="Пост")),
            ],
            options={"verbose_name": "Комментарий", "verbose_name_plural": "Комментарии", "ordering": ("-created_at", "-pk")},
        ),
    ]
