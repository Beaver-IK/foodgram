# Generated by Django 3.2 on 2025-03-16 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20250316_0044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeshortlink',
            name='original_url',
        ),
        migrations.AlterField(
            model_name='recipeshortlink',
            name='short_code',
            field=models.CharField(blank=True, max_length=3, unique=True),
        ),
    ]
