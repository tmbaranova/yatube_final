# Generated by Django 2.2.6 on 2021-04-02 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0018_comment_is_readed'),
    ]

    operations = [
        migrations.AddField(
            model_name='dislike',
            name='is_readed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='follow',
            name='is_readed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='like',
            name='is_readed',
            field=models.BooleanField(default=False),
        ),
    ]
