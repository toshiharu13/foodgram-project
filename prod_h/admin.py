from django.contrib import admin
from .models import Teg, ListOfIngridients, Amount, Recipe, Follow, Favorite, Cart


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

class FollowAdmin(admin.ModelAdmin):
    list_display = ("author", "user")
    search_fields = ("author",)
    # list_filter = ("name")
    empty_value_display = "-пусто-"

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")
    search_fields = ("user",)
    # list_filter = ("name")
    empty_value_display = "-пусто-"


class CardAdmin(admin.ModelAdmin):
    list_display = ("item", "customer")
    search_fields = ("item",)
    # list_filter = ("name")
    empty_value_display = "-пусто-"

admin.site.register(Teg, TegAdmin)
admin.site.register(ListOfIngridients, ListOfIgridientsAdmin)
admin.site.register(Amount, IngridientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CardAdmin)

