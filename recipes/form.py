from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'cooking_time', 'description', 'image')
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'cooking_time': forms.NumberInput(attrs={'value': 1}),
        }
    cooking_time = forms.IntegerField(required=True, min_value=1)
    image = forms.ImageField(required=True)
