from .models import ShopList, Tag


def get_shop_list(request):
    shop_list_count = None
    if request.user.is_authenticated:
        shop_list_count = ShopList.objects.filter(
            user=request.user).count()
    return {'shop_list_count': shop_list_count}


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ingredient_item = key.split('_')[1]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + ingredient_item]
    return ingredients


def get_all_tags():
    all_tags = Tag.objects.all()
    tags_list = []
    for tag in all_tags:
        tags_list.append(tag.value)
    return tags_list
