# Generated by Django 2.2.9 on 2020-12-07 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_suggestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='event_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='venue',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
