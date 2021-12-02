from django.db import models


class Mailing(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст')
    forms_count = models.PositiveIntegerField(verbose_name='Количество форм')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLink(models.Model):
    mailing = models.ForeignKey(
        to=Mailing,
        on_delete=models.CASCADE,
        related_name='links',
    )
    link = models.URLField(verbose_name='Ссылка')
    must_deleted = models.BooleanField(verbose_name='Должна ли удаляться?')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'


class User(models.Model):
    mailing_link = models.URLField(verbose_name='Ссылка')
    text = models.TextField(verbose_name='Текст')
    screenshot_link = models.URLField(verbose_name='Ссылка на скриншот')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
