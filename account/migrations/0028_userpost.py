# Generated by Django 4.1.5 on 2023-07-05 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_delete_friendrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
