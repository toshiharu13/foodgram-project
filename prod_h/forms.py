from django import forms
from .models import Recipe, Teg, ListOfIngridients, Ingredient

class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Teg.objects.all(),
        to_field_name='slug',
        required=False,
    )

    class Meta:
        model = Recipe
        fields = ['name', 'time', 'text', 'image', 'ingredients', "tags",]
