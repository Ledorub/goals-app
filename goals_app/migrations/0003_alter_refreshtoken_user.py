# Generated by Django 3.2.7 on 2021-11-03 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals_app', '0002_auto_20211102_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refreshtoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refresh_tokens', to=settings.AUTH_USER_MODEL),
        ),
    ]
