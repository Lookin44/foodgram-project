from django import template

from recipes.models import Favorite, ShopList, Subscription

register = template.Library()


@register.filter
def is_favorite(request, recipe):
    return Favorite.objects.filter(user=request.user, recipe=recipe).exists()


@register.filter
def is_follower(request, profile):
    return Subscription.objects.filter(user=request.user, author=profile
                                       ).exists()


@register.filter
def is_in_purchases(request, recipe):
    return ShopList.objects.filter(user=request.user, recipe=recipe).exists()


@register.filter()
def url_with_get(request, number):
    query = request.GET.copy()
    query['page'] = number
    return query.urlencode()


@register.filter
def correct_declension(obj_one, obj_two):
    remained = str(obj_one - obj_two)
    if remained[-1] == '1':
        return ''
    if remained[-1] in ['2', '3', '4']:
        return 'а'
    return 'ов'
