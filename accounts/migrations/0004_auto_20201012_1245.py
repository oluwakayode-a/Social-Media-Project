# Generated by Django 3.0.8 on 2020-10-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_interest_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.URLField(default='https://www.earthruh.com'),
        ),
    ]