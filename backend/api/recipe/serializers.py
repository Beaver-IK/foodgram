from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404
from django.db import transaction

from api.validators import PhotoValidator
from api.fields import Base64ImageField
from api.users.serializers import UserSerializer
from ingredient.models import RecipeIngredient, Ingredient
from recipe.models import Tag, Recipe
from api import constants as c

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для Тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug',)

class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания связей между рецептом и ингредиентами."""
    
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=[MinValueValidator(1)]
    )
    
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)

class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения связей между рецептом и ингредиентами."""
    
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredients.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецептов."""
    
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(
        source='recipeingredients',
        many=True,
        read_only=True
    )
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления рецептов."""
    
    ingredients = RecipeIngredientCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(
        name='recipe',
        required=True,
        validators=[
            PhotoValidator(size=c.MAX_FILE_SIZE),
            FileExtensionValidator(allowed_extensions=c.ALLOW_EXT)
        ]
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    """def validate_ingredients(self, value):
        ingredients = []
        for ingredient_data in value:
            print(ingredient_data)
            ingredient_id = ingredient_data['id']
            if ingredient_id in ingredients:
                raise serializers.ValidationError('Ингредиенты не должны дублироваться.')
            ingredients.append(ingredient_id)
        return value"""

#self, name, author, ingredients_data, tags_data,
#               image, text, cooking_time, **kwargs):


    def create(self, validated_data):
        image = validated_data.get('image')
        if image:
            image = self.fields['image'].run_validation(image)
        data = dict(
            name=validated_data.get('name'),
            author=self.context.get('request').user,
            ingredients_data=validated_data.get('ingredients'),
            tags_data=validated_data.get('tags'),
            image=image,
            text=validated_data.get('text'),
            cooking_time=validated_data.get('cooking_time')
        )
        recipe = Recipe.objects.create(data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        tags_data = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if tags_data is not None:
            instance.tags.set(tags_data)
        
        if ingredients_data is not None:
            instance.recipeingredients.all().delete()
            self.create_recipe_ingredients(instance, ingredients_data)
        
        instance.save()
        return instance