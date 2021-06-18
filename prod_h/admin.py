from django.contrib import admin
from .models import Teg, ListOfIngridients, Amount, Recipe


class TegAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color")
    search_fields = ("name",)
    #list_filter = ("name")
    empty_value_display = "-пусто-"

class ListOfIgridientsAdmin(admin.ModelAdmin):
    list_display = ( "pk", "name","units_of_measurement",)
    search_fields = ("name",)
    # list_filter = ("name")
    empty_value_display = "-пусто-"


class IngridientAdmin(admin.ModelAdmin):
    list_display = ("pk", "ingredient", "counts",)
    search_fields = ("name",)
    # list_filter = ("name")
    empty_value_display = "-пусто-"

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "time","pub_date")
    search_fields = ("name",)
    # list_filter = ("name")
    empty_value_display = "-пусто-"


admin.site.register(Teg, TegAdmin)
admin.site.register(ListOfIngridients, ListOfIgridientsAdmin)
admin.site.register(Amount, IngridientAdmin)
admin.site.register(Recipe, RecipeAdmin)

