# Generated by Django 2.2.6 on 2021-04-01 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20210401_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.TextField(blank=True, help_text='Введите заголовок', null=True, verbose_name='Заголовок'),
        ),
    ]