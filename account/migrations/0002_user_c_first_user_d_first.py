# Generated by Django 4.1.5 on 2023-03-07 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='C_first',
            field=models.IntegerField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='D_first',
            field=models.IntegerField(default=True),
        ),
    ]
