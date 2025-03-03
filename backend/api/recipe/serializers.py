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

from users.models import User

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для Тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug',)

class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания связей между рецептом и ингредиентами."""
    
    id = serializers.IntegerField(read_only=True, source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(read_only=True, source='ingredient.measurement_unit')
    
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления рецептов."""
    
    author = UserSerializer(read_only=True)
    image = Base64ImageField(
        name='recipe',
        validators=[
            FileExtensionValidator(allowed_extensions=c.ALLOW_EXT),
            PhotoValidator(size=c.MAX_FILE_SIZE)
        ]
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
    
    def get_is_favorited(self, obj: Recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.favorited_by.filter(id=user.id).exists()
    
    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.cart.recipes.filter(id=obj.id).exists()
    
    def create(self, validated_data):
        """Метод для создания нового рецепта."""
        self.initial_data['author'] = self.context.get('request').user
        image = self.fields['image'].run_validation(
            self.initial_data['image']
        )
        image.name = f'{self.initial_data["author"]}{image.name}'
        self.initial_data['image'] = image
        data = self.initial_data
        recipe = Recipe.objects.create(data)

        return recipe
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags, many=True).data
        representation['ingredients'] = RecipeIngredientCreateSerializer(
            instance.recipe_ingredients, many=True).data
        return representation
