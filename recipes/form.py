from django.forms import ModelForm
from django import forms

from .models import Recipe, Tag, Ingredient


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'tag',
            'ingredients',
            'cooking_time',
            'description',
            'image',
        )
