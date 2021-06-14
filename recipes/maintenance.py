def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ingredient_item = key.split('_')[1]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + ingredient_item]
    return ingredients
