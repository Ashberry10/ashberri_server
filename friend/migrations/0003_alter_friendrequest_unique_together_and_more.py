# Generated by Django 4.1.5 on 2023-06-11 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0002_rename_timestamp_friendrequest_created_at_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.RemoveField(
            model_name='friendrequest',
            name='accepted',
        ),
    ]