from django.shortcuts import get_object_or_404

from .models import Tag


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ingredient_name = key.split('_')[1]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + ingredient_name]
    return ingredients


def get_tags_for_edit(request):
    data = request.POST.copy()
    tags = []
    for value in ['lunch', 'dinner', 'breakfast']:
        if value in data and data.get(value) == 'on':
            tag = get_object_or_404(Tag, value=value)
            tags.append(tag)
    return tags
