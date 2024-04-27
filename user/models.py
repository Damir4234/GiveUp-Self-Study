from django.db import models
from django.contrib.auth.models import AbstractUser

from materials.models import NULLABLE, Answer


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, verbose_name='пароль')
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class CompletedTasks(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Урок')
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, verbose_name='Урок')
    is_correct = models.BooleanField(default=False)
