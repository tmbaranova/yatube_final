# Generated by Django 2.2.6 on 2021-03-23 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='Введите комментарий', verbose_name='Текст'),
        ),
    ]
