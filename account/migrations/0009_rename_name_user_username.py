# Generated by Django 4.1.5 on 2023-03-22 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_user_date_of_birth_user_day_user_month_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
    ]
