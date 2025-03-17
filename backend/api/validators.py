from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
from rest_framework import status
from rest_framework.request import Request
from rest_framework.serializers import ValidationError

from api.constants import MIN_INGREDIENTS_VALUE
from ingredient.models import Ingredient
from recipe.constants import MIN_COOKING_TIME
from users.constants import MAX_FILE_SIZE

User = get_user_model()


@deconstructible
class PhotoValidator:
    """Валидация поля фотографии."""

    def __init__(self, size):
        self.size = size

    def __call__(self, value):
        if value is None:
            raise ValidationError(
                detail={'avatar': 'Обязатльное поле'},
                code=status.HTTP_400_BAD_REQUEST
            )
        if value.size > MAX_FILE_SIZE:
            raise ValidationError(
                detail={f'Максимальный размер файла '
                        f'{MAX_FILE_SIZE / (1024 * 1024)} Мб'}
            )


@deconstructible
class RecipeDataValidator:
    """Валидация данных для создания и редактирования объекта рецепта."""

    def __init__(self, data):
        self.name = data.get('name', None)
        self.author = data.get('author', None)
        self.ingredients = data.get('ingredients', None)
        self.tags_data = data.get('tags', None)
        self.image = data.get('image', None)
        self.text = data.get('text', None)
        self.cooking_time = data.get('cooking_time', None)
        self.request = data.get('request', None)

    def __call__(self):
        self._name_validation()
        self._author_validator()
        self._ingredients_validator()
        self._tag_validator()
        self._image_validator()
        self._text_validator()
        self._cooking_time_validator()
        self._request_validator()

    def _name_validation(self):
        """"Валидация названия."""
        if not self.name:
            raise ValidationError(
                {'name': 'Отсутствует название рецепта'}
            )
        if not isinstance(self.name, str):
            raise ValidationError(
                {'name': 'Тип данных не соответвует ожидаемому "str"'}
            )

    def _author_validator(self):
        """Валидация автора."""
        if not self.author:
            raise ValidationError(
                {'author': 'У рецепта должен быть автор'}
            )
        if not isinstance(self.author, User):
            raise ValidationError(
                {'author': 'Тип данных не соответвует ожидаемому "User"'}
            )

    def _ingredients_validator(self):
        """Валидация ингредиентов."""

        if not self.ingredients:
            raise ValidationError(
                {'ingredients': 'Отсутсвуют ингредиенты'}
            )
        if not isinstance(self.ingredients, list):
            raise ValidationError(
                {'ingredients': 'Тип данных не соответвует ожидаемому "list"'}
            )
        if len(self.ingredients) < MIN_INGREDIENTS_VALUE:
            raise ValidationError(
                {'ingredients': (f'Необходимо минимум {MIN_INGREDIENTS_VALUE}'
                                 f'ингредиентов')}
            )
        ingredients_id = []
        for value in self.ingredients:
            ingredient_id = value.get('id')
            amount = value.get('amount')
            if not ingredient_id or not amount:
                raise ValidationError(
                    'Для каждого ингрединта должен быть указан '
                    'id и его количество в рецепте'
                )
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise ValidationError('Ингредиент не существует')
            ingredients_id.append(ingredient_id)
        if len(set(ingredients_id)) != len(self.ingredients):
            raise ValidationError(
                {'ingredients': 'Нельзя добавлять одинаковые ингредиенты'}
            )

    def _tag_validator(self):
        """Валидатор Тегов."""

        if not self.tags_data:
            raise ValidationError(
                {'tags': 'Необходимо указать теги'}
            )
        if not isinstance(self.tags_data, list):
            raise ValidationError(
                {'tags': 'Ожидается список Тегов'}
            )
        if len(set(self.tags_data)) != len(self.tags_data):
            raise ValidationError(
                {'tags': 'Нельзя указывать одинаковые теги к одному рецепту'}
            )

    def _image_validator(self):
        """Валидатор фотографии рецепта."""

        if self.request.method == 'PATCH' and self.image is None:
            return
        if not self.image:
            raise ValidationError(
                {'image': 'Отсутствует фото рецепта.'}
            )
        if not isinstance(self.image, ContentFile):
            raise ValidationError(
                {'image': 'Тип данных не соответвует ожидаемому "ContentFile"'}
            )

    def _text_validator(self):
        """валидатор описания."""
        if not self.text:
            raise ValidationError(
                {'text': 'Необходимо описание рецепта'}
            )
        if not isinstance(self.text, str):
            raise ValidationError(
                {'text': 'Тип данных не соответвует ожидаемому "str"'}
            )

    def _cooking_time_validator(self):
        """Валидатор времени приготовления."""
        if not self.cooking_time:
            raise ValidationError(
                {'cooking_time': 'Необходимо указать время приготовления'}
            )
        if not isinstance(self.cooking_time, int):
            raise ValidationError(
                {'cooking_time': 'Тип данных не соответвует ожидаемому "int"'}
            )
        if self.cooking_time < MIN_COOKING_TIME:
            raise ValidationError(
                {'cooking_time': (f'Время приготовления '
                                  f'не может быть меньше {MIN_COOKING_TIME}')}
            )

    def _request_validator(self):
        """Проверка передачи запроса в контекст."""
        if not self.request:
            raise ValidationError(
                {'request': 'Объект запроса не был передан в контекст'}
            )
        if not isinstance(self.request, Request):
            raise ValidationError(
                {'request': 'Тип данных не соответвует ожидаемому "Request"'}
            )
