from django.db import models
from django.contrib.auth.models import AbstractUser

from materials.models import Answer


class User(AbstractUser):
    pass


class CompletedTasks(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Урок')
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, verbose_name='Урок')
    is_correct = models.BooleanField(default=False)
