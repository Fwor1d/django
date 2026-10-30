from django.conf import settings
from django.db import models
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="profile", verbose_name="Пользователь")
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)
    bio = models.TextField("О себе", blank=True)
    location = models.CharField("Город", max_length=100, blank=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    @property
    def avatar_url(self):
        if self.avatar:
            try:
                return self.avatar.url
            except ValueError:
                pass
        return static("img/default_avatar.png")

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
