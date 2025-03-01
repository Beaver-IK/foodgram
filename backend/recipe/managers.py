from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from ingredient.models import Ingredient, RecipeIngredient
from recipe.models import Recipe


class RecipeManager(models.Manager):
    
    
    def create(self, data, **kwargs):
        
        from recipe.models import Tag
        from ingredient.models import RecipeIngredient
        
        name = data['name']
        author = data['author']
        ingredients_data = data['ingredients_data']
        tags_data = data['tags_data']
        image = data['image']
        text = data['text']
        cooking_time = data['cooking_time']
        
        if not name:
            raise ValidationError(
                {'name': 'Необходимо указать название рецепта'}
            )
        if not author:
            raise ValidationError({'author': 'У рецепта должен быть автор'})
        if not ingredients_data:
            raise ValidationError(
                {'ingredients_data': 'Нужны ингредиенты'}
            )
        if not tags_data:
            raise ValidationError({'tags_data':'Нужны теги'})
        if not image:
            raise ValidationError({'image': 'Нужна фотография блюда'})
        if not text:
            raise ValidationError({'text': 'Добавьте описание рецепта'})
        if not cooking_time:
            raise ValidationError(
                {'cooking_time': 'Добавьте время приготовления'}
            )
        with transaction.atomic():
            recipe = self.model(
                name=name,
                author=author,
                image=image,
                text=text,
                cooking_time=cooking_time,
                **kwargs)
            recipe.save()
            
            for data in ingredients_data:
                ingredient_id = data.get('id')
                amount = data.get('amount')
                
                if not ingredient_id or not amount:
                    raise ValidationError(
                        'Для каждого ингрединта должен быть указан '
                        'id и его количество в рецепте'
                    )
                ingredient = get_object_or_404(Ingredient, id=ingredient_id)
                recipe.ingredients.add
                recipe.ingredients.add(
                    ingredient,
                    through_defaults={'amount': amount}
                )
                
            if all(isinstance(tag, int) for tag in tags_data):
                tags = Tag.objects.filter(id__in=tags_data)
                if len(tags_data) != len(set(tags)):
                    raise ValidationError('Есть несуществующие теги')
            elif all(isinstance(tag, Tag) for tag in tags_data):
                tags = tags_data
            
            recipe.tags.set(tags)

        return recipe