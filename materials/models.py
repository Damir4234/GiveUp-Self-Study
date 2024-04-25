from django.db import models

from user.models import User


NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    """Модель курса"""
    title = models.CharField(
        max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Урок')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """Модель урока - теоретический материал, относится к одному конкретному курсу"""
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(
        max_length=255, verbose_name='Название')
    content = models.TextField(verbose_name='Материал урока', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Answer(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name='урок')
    question = content = models.TextField(
        verbose_name='Материал урока')
    correct_answer = models.CharField(
        max_length=150, verbose_name='Название')
