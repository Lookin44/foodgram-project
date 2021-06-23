from django import template

from recipes.models import Favorite, ShopList, Subscription

register = template.Library()

ONE_RECIPE = 'рецепт'
FEW_RECIPES = 'рецепта'
RECIPES = 'рецептов'


@register.filter
def is_favorite(request, recipe):
    return Favorite.objects.filter(user=request.user, recipe=recipe).exists()


@register.filter
def is_follower(request, profile):
    return Subscription.objects.filter(
        user=request.user, author=profile).exists()


@register.filter
def is_in_purchases(request, recipe):
    return ShopList.objects.filter(user=request.user, recipe=recipe).exists()


@register.filter()
def url_with_get(request, number):
    query = request.GET.copy()
    query['page'] = number
    return query.urlencode()


@register.filter
def correct_declension(all_recipes):
    all_recipes -= 3
    word = RECIPES
    if (all_recipes % 10 == 1) and (all_recipes % 100 != 11):
        word = ONE_RECIPE
    elif (
            (all_recipes % 10 >= 2) and
            (all_recipes % 10 <= 4) and
            (all_recipes % 100 < 10 or all_recipes % 100 >= 20)
    ):
        word = FEW_RECIPES
    return f'Еще {all_recipes} {word}...'
