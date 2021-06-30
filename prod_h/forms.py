from django import forms
from django.shortcuts import get_object_or_404

from .models import Recipe, Tag
from .utils import get_ingredients, get_tags


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'time', 'text', 'image', ]

    widgets = {
        'name': forms.TextInput(attrs={
            'class': 'form__input'
        }),
        'time': forms.TextInput(attrs={
            'class': 'form__input'
        }),
        'text': forms.Textarea(attrs={
            'rows': 8,
            'class': 'form__textarea'
        }),
    }

    def save(self, request=None, *args, **kwargs):
        instance = super().save(commit=False)
        instance.author = request.user
        instance.save()
        # Adds tags to the recipe
        for name_tag in get_tags(request):
            tag_from_bd = get_object_or_404(Tag, name=name_tag)
            instance.tags.add(tag_from_bd.id)
        # Adds ingredients to the recipe
        list_of_ingredients = get_ingredients(request, instance)
        for ingr in list_of_ingredients:
            instance.ingredients.add(ingr)
        return instance
