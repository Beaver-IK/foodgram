from django.db import models, transaction

from api.models import RecipeShortLink
from api.validators import RecipeDataValidator
from ingredient.models import RecipeIngredient


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

            RecipeIngredient.objects.bulk_create(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient_id=values.get('id'),
                    amount=values.get('amount')
                ) for values in ingredients_data
            )

            recipe.tags.set(tags_data)

            short_link = RecipeShortLink.objects.create(
                recipe=recipe,
            )
            short_link.save()

            return recipe
