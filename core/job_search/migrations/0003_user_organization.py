# Generated by Django 5.0.4 on 2024-05-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_search', '0002_user_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
