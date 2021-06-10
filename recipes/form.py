from django.forms import ModelForm
from django import forms

from .models import Recipe


class RecipeCreateForm(ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'tags',
            'cooking_time',
            'description',
            'image',
        )
        widgets = {'tag': forms.CheckboxSelectMultiple()}


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'description', 'image',)
