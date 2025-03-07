# Generated by Django 3.2 on 2025-02-28 19:13

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_alter_recipe_is_active'),
        ('ingredient', '0003_rename_quantity_recipeingredient_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'default_related_name': 'recipeingredients', 'verbose_name': 'Ингредиент рецепта', 'verbose_name_plural': 'Ингредиенты рецепта'},
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(help_text='Укажите количество', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Общее количество'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipeingredients', to='ingredient.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipeingredients', to='recipe.recipe'),
        ),
    ]
