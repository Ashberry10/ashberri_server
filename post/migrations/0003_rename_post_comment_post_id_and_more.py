# Generated by Django 4.1.5 on 2023-10-28 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='post_id',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='user_id',
        ),
    ]
