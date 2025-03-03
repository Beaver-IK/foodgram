from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class RecipeManager(models.Manager):
    
    
    """def create(self, **kwargs):
        return super().create(**kwargs)"""
    
    def create(self, data):
        
        from recipe.models import Tag
        from ingredient.models import RecipeIngredient
        from ingredient.models import Ingredient
        
        name = data.get('name')
        author = data.get('author')
        ingredients_data = data.get('ingredients')
        tags_data = data.get('tags')
        image = data.get('image')
        text = data.get('text')
        cooking_time = data.get('cooking_time')
        
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
                cooking_time=cooking_time
            )
            recipe.save()
            for value in ingredients_data:
                ingredient_id = value.get('id')
                amount = value.get('amount')
                
                if not ingredient_id or not amount:
                    raise ValidationError(
                        'Для каждого ингрединта должен быть указан '
                        'id и его количество в рецепте'
                    )
                ingredient = get_object_or_404(Ingredient, id=ingredient_id)
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount)
                recipe.ingredients.add(ingredient)
                
            if all(isinstance(tag, int) for tag in tags_data):
                tags = Tag.objects.filter(id__in=tags_data)
                if len(tags_data) != len(set(tags)):
                    raise ValidationError('Есть несуществующие теги')
            elif all(isinstance(tag, Tag) for tag in tags_data):
                tags = tags_data
            
            recipe.tags.set(tags)
            
            return recipe