from django import forms
from .models import Recipe, Teg

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['name', 'time', 'text', 'image', 'ingridients', "teg",]