# Generated by Django 3.2.9 on 2021-11-29 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals_app', '0006_auto_20211130_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='counter', to='goals_app.task'),
        ),
    ]
