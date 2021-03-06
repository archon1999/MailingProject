# Generated by Django 3.2 on 2021-12-02 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='link',
        ),
        migrations.RemoveField(
            model_name='mailing',
            name='must_deleted',
        ),
        migrations.AddField(
            model_name='mailing',
            name='title',
            field=models.CharField(default='123', max_length=255, verbose_name='Заголовок'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='MailingLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(verbose_name='Ссылка')),
                ('must_deleted', models.BooleanField(verbose_name='Должна ли удаляться?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='backend.mailing')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
            },
        ),
    ]
