import csv
import os
from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError

from api.recipe.serializers import RecipeStripSerializer
from api.users.serializers import ExtendUserSerializer
from ingredient.models import RecipeIngredient

User = get_user_model()


class OrderGenerator:
    """Генератор заказа продуктов из корзины."""

    class Data:
        file_format = None
        file_name = None
        ingredients_sum = None

    def __init__(self, cart, file_format):

        self.cart = cart
        self.Data.file_format = file_format
        self.owner = cart.owner
        self._get_order()

    def _get_data(self):
        return self.Data.ingredients_sum.items()

    def _get_order(self):
        ingredients_sum = (
            RecipeIngredient.objects.
            filter(recipe__in=self.cart.recipes.all()).
            values('ingredient__name', 'ingredient__measurement_unit').
            annotate(total_amount=Sum('amount'))
        )

        ingredients_sum = tuple(
            (i,
             item['ingredient__name'],
             item['ingredient__measurement_unit'],
             item['total_amount']) for i, item in enumerate(ingredients_sum,
                                                            start=1)
        )

        if ingredients_sum:
            self.Data.ingredients_sum = ingredients_sum

    def run_generator(self):
        """Запуск генератора файла."""

        self.Data.file_name = f'Order_{self.owner}_{datetime.now()}'

        get_response = dict(
            txt=self._get_txt(),
            pdf=self._get_pdf(),
            csv=self._get_csv(),
        )
        response = get_response.get(self.Data.file_format)
        if not response:
            raise ValidationError(
                'Запрашиваемый формат не поддерживается',
                status=status.HTTP_400_BAD_REQUEST
            )
        return response

    def _get_pdf(self):
        """Внутренний метод для формирования ответа с файлом pdf."""
        font_path = os.path.join(settings.BASE_DIR, 'fonts', 'greca.ttf')
        logo_path = os.path.join(settings.BASE_DIR, 'logo.png')

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        pdfmetrics.registerFont(TTFont('Greca', font_path))
        p.setFont('Greca', 20)

        p.drawImage(logo_path, 50, 725, width=100, height=100)

        y_position = 680
        p.drawString(250, 710, 'Список покупок')

        p.line(50, 700, 550, 700)

        for num, name, unit, total_amount in self.Data.ingredients_sum:
            text = f'{num}. {name} — {total_amount} {unit}'
            y_position -= 20
            p.drawString(100, y_position, text)
        p.showPage()
        p.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="{self.Data.file_name}.pdf"'
        )
        return response

    def _get_csv(self):
        """Внутренний метод для формирования ответа с файлом csv."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            f'attachment; filename="{self.Data.file_name}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            ['п/п', 'Название', 'Единица измерения', 'Общее кол-во']
        )

        for num, name, unit, total_amount in self.Data.ingredients_sum:
            writer.writerow([num, name, unit, total_amount])

        return response

    def _get_txt(self):
        """Внутренний метод для формирования ответа с файлом txt."""
        shopping_list = "Список покупок:\n\n"
        for num, name, unit, total_amount in self.Data.ingredients_sum:
            shopping_list += f'{num}. {name} — {total_amount} {unit}\n'

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="{self.Data.file_name}.txt"'
        )
        return response


class BaseResponseGenerator:
    """Базовый класс для генераторов HTTP ответов."""

    exists = True
    response_map: dict = {}
    context: dict = {}

    NO_CONTENT = Response(status=status.HTTP_204_NO_CONTENT)
    RECIPE_SERIALIZER = RecipeStripSerializer
    USERSERIALIZER = ExtendUserSerializer

    def __init__(self, target_item, container, queryset, req_method, context=None):

        self.target_item = target_item
        self.container = container
        self.queryset = queryset
        self.req_method = req_method
        if context:
            self.context = context
        self._set_exists()

    def _set_exists(self):
        """Установка флага наличия объекта базе данных."""

        self.exists = self.queryset.filter(id=self.target_item.id).exists()

    def _validate(self):
        """Проверка корректности запроса."""
        if self.req_method == 'POST' and self.exists:
            raise ValidationError('Объект уже добавлен',)
        if self.req_method == 'DELETE' and not self.exists:
            raise ValidationError('Объект отсутствует')

    def get_response(self):
        """Получение HTTP-ответа."""
        self._validate()
        if self.req_method == 'POST':
            return self._add()
        return self._delete()

    def _add(self):
        """Добавление объекта (реализуется в дочерних классах)."""
        raise NotImplementedError

    def _delete(self):
        """Удаление объекта (реализуется в дочерних классах)."""
        raise NotImplementedError


class SubscriptionResponseGenerator(BaseResponseGenerator):
    """Генератор добавления/удаления подписок."""

    def _add(self):
        """Добавление подписки."""
        self.container.subscriptions.add(self.target_item)
        serializer = self.USERSERIALIZER(self.target_item, context=self.context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete(self):
        """Удаление подписки."""
        self.container.subscriptions.remove(self.target_item)
        return self.NO_CONTENT

    def _validate(self):
        super()._validate()
        if self.target_item == self.container:
            raise ValidationError('Нельзя подписаться или удалить себя')


class FavoriteResponseGenerator(BaseResponseGenerator):
    """Генератор добавления/удаления рецепта в избранное."""

    def _add(self):
        """Добавление рецепта в избранное."""
        self.container.favourites.add(self.target_item)
        serializer = self.RECIPE_SERIALIZER(self.target_item, context=self.context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete(self):
        """Удаление рецепта из избранного."""
        self.container.favourites.remove(self.target_item)
        return self.NO_CONTENT


class CartResponseGenerator(BaseResponseGenerator):
    """Генератор добавления/удаления рецепта в конзину."""

    def _add(self):
        """Добавление рецепта в корзину."""
        self.container.recipes.add(self.target_item)
        serializer = self.RECIPE_SERIALIZER(self.target_item, context=self.context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete(self):
        """Удаление рецепта из корзины."""
        self.container.recipes.remove(self.target_item)
        return self.NO_CONTENT
