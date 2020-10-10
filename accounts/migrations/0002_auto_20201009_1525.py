# Generated by Django 3.0.8 on 2020-10-09 14:25

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interests', multiselectfield.db.fields.MultiSelectField(choices=[('music', 'Music'), ('photography', 'Photography'), ('acting', 'Acting'), ('art', 'Art'), ('travel', 'Travel'), ('sports', 'Sports'), ('dance', 'Dance'), ('architectures', 'Architectures'), ('humanity', 'Humanity'), ('food', 'Food'), ('fashion', 'Fashion'), ('cricket', 'Cricket'), ('comedy', 'comedy'), ('education', 'Education'), ('poetry', 'Poetry'), ('spiritual', 'Spiritual'), ('fitness', 'Fitness'), ('auto', 'Auto/Moto')], max_length=139)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='interests',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='accounts.Interest'),
        ),
    ]