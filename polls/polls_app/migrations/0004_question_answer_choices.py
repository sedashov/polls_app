# Generated by Django 2.2.10 on 2020-11-12 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0003_auto_20201112_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_choices',
            field=models.TextField(default=''),
        ),
    ]
