# Generated by Django 3.2.6 on 2021-12-03 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20211203_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermailingform',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
