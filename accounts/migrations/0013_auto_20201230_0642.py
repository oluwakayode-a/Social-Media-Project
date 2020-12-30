# Generated by Django 2.2.9 on 2020-12-30 05:42

import accounts.models
from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20201214_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=encrypted_model_fields.fields.EncryptedTextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=encrypted_model_fields.fields.EncryptedDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=accounts.models.EncryptedPhoneField(),
        ),
    ]
