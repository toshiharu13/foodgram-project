from django import forms

from .models import Recipe


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
