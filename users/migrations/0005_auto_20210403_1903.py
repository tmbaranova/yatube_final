# Generated by Django 2.2.6 on 2021-04-03 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210401_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='media/default.jpg', upload_to='users/'),
        ),
    ]
