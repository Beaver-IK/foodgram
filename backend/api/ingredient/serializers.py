from rest_framework.serializers import ModelSerializer

from ingredient.models import Ingredient


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id',
                  'name',
                  'measurement_unit',)
