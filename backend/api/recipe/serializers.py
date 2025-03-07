from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from api import constants as c
from api.fields import Base64ImageField
from api.users.serializers import UserSerializer
from api.validators import PhotoValidator, RecipeDataValidator
from ingredient.models import Ingredient, RecipeIngredient
from recipe.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для Тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug',)

class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для создания связей между рецептом и ингредиентами."""
    
    id = serializers.IntegerField(read_only=True, source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )
    
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
 
    def validate(self, attrs):
        attrs['ingredients'] = self.initial_data.get('ingredients')
        attrs['author'] = self.context.get('request').user
        attrs['image'] = self.fields['image'].run_validation(
            self.initial_data['image']
        )
        attrs['image'].name = (
            f'{attrs["author"]}{attrs["image"].name}'
        )
        attrs['request'] = self.context.get('request')
        validator = RecipeDataValidator(data=attrs)
        validator()
        return attrs

    def create(self, validated_data):
        """Cоздание нового рецепта."""
        try:
            recipe = Recipe.objects.create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(
                f'Ошибка: {e}'
            )
        return recipe
    
    def update(self, instance: Recipe, validated_data):
        instance.name = validated_data.get(
            'name',
            instance.name
        )
        instance.text = validated_data.get(
            'text',
            instance.text
        )
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.image = validated_data.get(
            'image',
            instance.image
        )
        instance.save()
        tags_data = validated_data.pop('tags', None)
        if tags_data:
            instance.tags.set(tags_data)
        ingredients_data = validated_data.pop('tags', None)
        if ingredients_data:
            self._update_recipeingredients(instance, ingredients_data)
            
        return instance
    
    def _update_recipeingredients(self, recipe, ingredients_data):
        """Метод для обновления данных в связанной модели RecipeIngredient."""
        
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        
        for values in ingredients_data:
            ingredient = Ingredient.objects.get(id=values.get('id'))
            amount = values.get('amount')
            Recipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags, many=True).data
        representation['ingredients'] = RecipeIngredientSerializer(
            instance.recipe_ingredients, many=True).data
        return representation


class RecipeStripSerializer(serializers.ModelSerializer):
    """Сериализвтор для рецепта с ограниченным выводом данных."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )