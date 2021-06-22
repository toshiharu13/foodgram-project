import importlib
from prod_h.models import Amount, ListOfIngridients
from decimal import Decimal

from django.shortcuts import get_object_or_404

module = importlib.import_module('.settings', 'foodgram-project')

def get_tags(request):
    # Get tags list
    tags_list = []
    for key in request.POST.keys():
        if key in module.TAGS:
            tags_list.append(key)
    return tags_list

def get_ingredients(request, recipe):
    # Add Ingredients to New Recipe.
    ist_of_ingredients = []
    name_of_ingredient = None
    for key, value in request.POST.items():
        if 'nameIngredient' in key:
            name_of_ingredient = value
        if 'valueIngredient' in key:
            #amount = Decimal(value.replace(',', '.'))
            amount = value
            ingredient = get_object_or_404(ListOfIngridients, name=name_of_ingredient)
            Amount.objects.get_or_create(
                    ingredient=ingredient,
                    recipe=recipe,
                    counts=amount)[0]
            ist_of_ingredients.append(ingredient)
    return ist_of_ingredients

def tags_filter(request):
    # Get actual tags
    tags_list = request.GET.getlist('tag', module.TAGS)
    return tags_list