from django.contrib import admin

from .models import (Amount, Cart, Favorite, Follow, ListOfIngridients, Recipe,
                     Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class ListOfIgridientsAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "units_of_measurement",)
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class IngridientAdmin(admin.ModelAdmin):
    list_display = ("pk", "ingredient", "counts",)
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "time", "pub_date", "slug")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class FollowAdmin(admin.ModelAdmin):
    list_display = ("author", "user", "pk")
    search_fields = ("author",)
    empty_value_display = "-пусто-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("recipe", "user")
    search_fields = ("user",)
    empty_value_display = "-пусто-"


class CardAdmin(admin.ModelAdmin):
    list_display = ("item", "customer")
    search_fields = ("item",)
    empty_value_display = "-пусто-"


admin.site.register(Tag, TagAdmin)
admin.site.register(ListOfIngridients, ListOfIgridientsAdmin)
admin.site.register(Amount, IngridientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CardAdmin)
