from django.shortcuts import get_object_or_404

from .models import Tag


def get_tags_for_edit(request):
    tags_list = []
    for i, j in request.POST.items():
        if j == 'on':
            tags_list.append(i)
    return tags_list


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ingredient_item = key.split('_')[1]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + ingredient_item]
    return ingredients
