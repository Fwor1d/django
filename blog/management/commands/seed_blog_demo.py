from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from blog.models import Post


class Command(BaseCommand):
    help = "Добавить 12 учебных постов для демонстрации поиска и пагинации (без дубликатов)"

    def handle(self, *args, **options):
        author = get_user_model().objects.order_by("pk").first()
        if not author:
            raise CommandError("Сначала создайте пользователя через createsuperuser или signup.")
        themes = [
            ("Знакомство с Django", "Фреймворк Django помогает быстро создавать сайты на Python."),
            ("Маршруты и представления", "Файл urls.py связывает адрес страницы с view-функцией."),
            ("HTML-шаблоны", "Общий шаблон base.html позволяет повторно использовать разметку."),
            ("Статические файлы CSS", "Через static в проект добавляется оформление и изображения."),
            ("Модели Django ORM", "Post хранит заголовок, содержание и дату публикации."),
            ("Админ-панель Django", "Администратор создаёт, редактирует и публикует записи."),
            ("Динамические URL", "Маршруты позволяют открывать страницы отдельных записей."),
            ("Формы и проверка данных", "ModelForm создаёт формы и проверяет введённые поля."),
            ("Комментарии к постам", "Зарегистрированные пользователи обсуждают записи."),
            ("Поиск по блогу", "Поиск использует Q и icontains по тексту и заголовку."),
            ("Регистрация и профили", "В Django доступны авторизация и личный кабинет."),
            ("Bootstrap и адаптивность", "Карточки и сетка Bootstrap подходят для телефона."),
        ]
        created_count = 0
        for title, body in themes:
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(title=title, summary=body, body=body + "\n\nЭта запись создана для демонстрации учебного проекта.", author=author, is_published=True)
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Добавлено {created_count} учебных публикаций."))
