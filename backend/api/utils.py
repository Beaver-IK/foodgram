from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
import csv
from rest_framework.validators import ValidationError
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from django.conf import settings
from datetime import datetime


from ingredient.models import RecipeIngredient


class OrderGenerator:
    """Генератор заказов для """
    
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
        recipes = self.cart.recipes.all()

        ingredients_sum = dict()
        counter = 1
        
        for recipe in recipes:
            resipe_ingrediens = RecipeIngredient.objects.filter(recipe=recipe)
            for item in resipe_ingrediens:
                name = item.ingredient.name
                measurement_unit = item.ingredient.measurement_unit
                amount = item.amount
                num = counter
                
                key = (num, name, measurement_unit)
                if key in ingredients_sum:
                    ingredients_sum[key] += amount
                else:
                    ingredients_sum[key] = amount
        
        if ingredients_sum:
            self.Data.ingredients_sum = ingredients_sum
    
    def run_generator(self):
        """Запуск генератора файла."""
        if not all(value is not None for value in self.Data.__dict__.values()):
            return Response('Корзина пуста', status=status.HTTP_200_OK)

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
        
        for (num, name, unit), total_amount in self._get_data():
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

        for (num, name, unit), total_amount in self._get_data():
            writer.writerow([num, name, unit, total_amount])

        return response
    
    def _get_txt(self):
        """Внутренний метод для формирования ответа с файлом csv."""
        shopping_list = "Список покупок:\n\n"
        for (num, name, unit), total_amount in self._get_data():
            shopping_list += f'{num}. {name} — {total_amount} {unit}\n'

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="{self.Data.file_name}.txt"'
        )
        return response