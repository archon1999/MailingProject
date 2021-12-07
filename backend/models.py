from django.db import models
from django.contrib import admin
from django.utils.html import format_html


class Mailing(models.Model):
    title = models.CharField(max_length=255, unique=True,
                             verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст')
    forms_count = models.PositiveIntegerField(verbose_name='Количество форм')
    mass = models.FileField(upload_to='mass', null=True, blank=True,
                            verbose_name='Массовое добавление')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if self.mass:
            with open(self.mass.name, encoding='utf-8') as file:
                for link in file.read().split('\n'):
                    self.links.create(link=link)

            self.mass = None

        return result

    def __str__(self):
        return self.title


class MailingLink(models.Model):
    mailing = models.ForeignKey(
        to=Mailing,
        on_delete=models.CASCADE,
        related_name='links',
    )
    link = models.URLField(verbose_name='Ссылка')
    must_deleted = models.BooleanField(default=True,
                                       verbose_name='Должна ли удаляться?')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'


class ProfileStatistics(models.Model):
    profile = models.CharField(max_length=1000, verbose_name='Профиль')

    @admin.display(description='Количество заявок')
    def get_applications_count(self):
        return UserMailingForm.objects.filter(
            user__profile=self.profile,
        ).count()

    @admin.display(description='Принято')
    def get_adopted_count(self):
        return UserMailingForm.objects.filter(
            user__profile=self.profile,
            completed=True,
        ).count()

    @admin.display(description='Отклонено')
    def get_unaccepted_count(self):
        return UserMailingForm.objects.filter(
            user__profile=self.profile,
            completed=False,
        ).count()

    @admin.display(description='В процентах')
    def get_adopted_percentage(self):
        if self.get_applications_count() == 0:
            return 'Неизвестно'

        percentage = 100*self.get_adopted_count()/self.get_applications_count()
        return str(round(percentage, 2)) + '%'

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'


class User(models.Model):
    profile = models.CharField(max_length=1000, verbose_name='Профиль')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE,
                                verbose_name='Рассылка')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @admin.display(description='Инфо')
    def info(self):
        html = f'<b>{self.profile}</b><br>'
        for index, form in enumerate(self.forms.all(), 1):
            html += f'<a href="/{form.screenshot.name}">Скриншот {index}</a><br>'

        return format_html(html)
 
    def save(self, *args, **kwargs):
        ProfileStatistics.objects.get_or_create(profile=self.profile)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.profile


class UserMailingForm(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='forms',
    )
    mailing_link = models.URLField(verbose_name='Ссылка')
    text = models.TextField(verbose_name='Текст')
    screenshot = models.ImageField(upload_to='screenshots')
    completed = models.BooleanField(default=True, verbose_name='Выполнено')
