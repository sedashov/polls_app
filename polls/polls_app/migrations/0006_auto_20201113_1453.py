# Generated by Django 2.2.10 on 2020-11-13 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0005_auto_20201112_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_choices',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='userquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polls_app.Question'),
        ),
        migrations.AlterField(
            model_name='userquestion',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
