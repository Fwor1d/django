from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    group = models.CharField(max_length=20)
    email = models.EmailField()
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# Create your models here.
