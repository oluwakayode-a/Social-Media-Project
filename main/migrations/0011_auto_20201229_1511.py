# Generated by Django 2.2.9 on 2020-12-29 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20201210_1445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created']},
        ),
        migrations.RemoveField(
            model_name='suggestion',
            name='title',
        ),
        migrations.AddField(
            model_name='suggestion',
            name='category',
            field=models.CharField(choices=[('bug_report', 'Bug Report'), ('improvement', 'Improvement')], default='bug_report', max_length=10),
            preserve_default=False,
        ),
    ]
