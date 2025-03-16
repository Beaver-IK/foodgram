from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.shortcuts import get_object_or_404

from api.models import RecipeShortLink
from api.validators import RecipeDataValidator
from ingredient.models import Ingredient, RecipeIngredient


class RecipeManager(models.Manager):
    """Менеджер для модели рецепта."""

    def create(self, data):

        validator = RecipeDataValidator(data=data)
        validator()

        name = data.get('name')
        author = data.get('author')
        ingredients_data = data.get('ingredients')
        tags_data = data.get('tags')
        image = data.get('image')
        text = data.get('text')
        cooking_time = data.get('cooking_time')

        with transaction.atomic():
            recipe = self.model(
                name=name,
                author=author,
                image=image,
                text=text,
                cooking_time=cooking_time
            )
            recipe.save()

            recipe_ingredients = []

            for value in ingredients_data:
                ingredient_id = value.get('id')
                amount = value.get('amount')
                if not ingredient_id or not amount:
                    raise ValidationError(
                        'Для каждого ингрединта должен быть указан '
                        'id и его количество в рецепте'
                    )
                ingredient = get_object_or_404(Ingredient, id=ingredient_id)
                recipe_ingredients.append(RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount)
                )
            RecipeIngredient.objects.bulk_create(recipe_ingredients)

            recipe.tags.set(tags_data)

            short_link = RecipeShortLink.objects.create(
                recipe=recipe,
            )
            short_link.save()

            return recipe
