# Generated by Django 3.2 on 2025-02-27 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0002_recipeingredient_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='quantity',
            new_name='amount',
        ),
    ]
