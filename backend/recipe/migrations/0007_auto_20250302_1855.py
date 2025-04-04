# Generated by Django 3.2 on 2025-03-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0006_auto_20250302_1855'),
        ('recipe', '0006_alter_recipe_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to='recipes/foto/', verbose_name='Фото рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, related_name='recipes', through='ingredient.RecipeIngredient', to='ingredient.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='recipe.Tag', verbose_name='Теги'),
        ),
    ]
