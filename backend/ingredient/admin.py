from django.contrib import admin

from ingredient.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit_display')
    search_fields = ('name', 'id',)
    list_filter = ('measurement_unit',)
    ordering = ('name',)
    save_on_top = True
    list_per_page = 20

    @admin.display(description='Единица измерения')
    def measurement_unit_display(self, obj):
        return obj.get_measurement_unit_display()
