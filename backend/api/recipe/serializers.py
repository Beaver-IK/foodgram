from rest_framework import serializers
from django.core.validators import FileExtensionValidator


from api.validators import PhotoValidator
from api.fields import Base64ImageField
from api.users.serializers import UserSerializer
from recipe.models import Tag, Recipe
from api import constants as c

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    # ingredients = IngredientSerializer(many=True)
    # is_favorited = 
    # is_in_shopping_cart =
    # name =
    image = Base64ImageField(
        validators=[
            PhotoValidator(size=c.MAX_FILE_SIZE),
            FileExtensionValidator(allowed_extensions=c.ALLOW_EXT)
        ]
    )
    # text = 
    # cooking_time = 
    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time',)
