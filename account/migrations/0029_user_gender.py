# Generated by Django 4.1.5 on 2023-07-25 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_userpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.IntegerField(default=0),
        ),
    ]