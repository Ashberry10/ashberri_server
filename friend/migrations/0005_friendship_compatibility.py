# Generated by Django 4.1.5 on 2023-09-06 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0004_rename_friendrequest_friendship'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='compatibility',
            field=models.IntegerField(default=1),
        ),
    ]
