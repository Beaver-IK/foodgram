from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from api import constants as c
from api.fields import Base64ImageField
from api.users.serializers import UserSerializer
from api.validators import PhotoValidator, RecipeDataValidator
from ingredient.models import RecipeIngredient
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
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецепта."""

    tags = TagSerializer(many=True)
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True,
                                             source='recipe_ingredients')

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
        read_only_fields = fields

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


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления рецептов."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(
        name='recipe',
        validators=[
            FileExtensionValidator(allowed_extensions=c.ALLOW_EXT),
            PhotoValidator(size=c.MAX_FILE_SIZE)
        ]
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

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

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)
        instance.tags.set(tags_data)
        self._update_recipeingredients(instance, ingredients_data)

        return instance

    def _update_recipeingredients(self, recipe, ingredients_data):
        """Метод для обновления ингредентов рецепта."""

        RecipeIngredient.objects.filter(recipe=recipe).delete()

        recipe_ingredients = []

        for values in ingredients_data:
            ingredient = values.get('id')
            amount = values.get('amount')
            recipe_ingredients.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient_id=ingredient,
                    amount=amount
                )
            )
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data


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
