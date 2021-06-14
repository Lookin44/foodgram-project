import csv
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .form import RecipeForm
from .maintenance import get_ingredients
from .models import (Amount, Favorite, Ingredient, Recipe, ShopList,
                     Subscription, Tag, User)


def index(request):
    tags_list = request.GET.getlist('tags')

    if not tags_list:
        tags_list = ['breakfast', 'lunch', 'dinner']

    all_tags = Tag.objects.all()

    recipe_list = Recipe.objects.filter(
        tags__value__in=tags_list
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'paginator': paginator,
               'page': page,
               'all_tags': all_tags,
               'tags_list': tags_list}
    return render(request, 'index.html', context)


def profile_view(request, username):
    tags_list = request.GET.getlist('tags')

    if not tags_list:
        tags_list = ['breakfast', 'lunch', 'dinner']

    all_tags = Tag.objects.all()

    profile = get_object_or_404(User, username=username)

    recipes_profile = Recipe.objects.filter(
        author=profile
    ).filter(
        tags__value__in=tags_list
    ).select_related(
        'author'
    ).distinct()

    follow_button = False

    if request.user.is_authenticated and request.user != profile:
        follow_button = True

    paginator = Paginator(recipes_profile, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'paginator': paginator,
               'page': page,
               'profile': profile,
               'follow_button': follow_button,
               'all_tags': all_tags,
               'tags_list': tags_list}
    return render(request, 'profile.html', context)


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'recipe_main.html', context)


def ingredients(request):
    text = request.GET.get('query')
    if text:
        ingredient_list = list(Ingredient.objects.filter(
            title__istartswith=text).values())
        return JsonResponse(ingredient_list, safe=False)
    else:
        raise ValueError('error: empty query')


@login_required()
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        ingredients_add = get_ingredients(request)
        for title, quantity in ingredients_add.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            ingredient_item = Amount(recipe=recipe,
                                     quantity=quantity,
                                     ingredient=ingredient)
            ingredient_item.save()
        form.save_m2m()
        return redirect('recipe', recipe_id=recipe.id)
    context = {'form': form, 'new': True}
    return render(request, 'new_recipe.html', context)


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe_id)

    form = RecipeForm(request.POST,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        change_recipe = form.save(commit=False)
        change_recipe.author = request.user
        change_recipe.save()
        change_recipe.recipe_amount.all().delete()
        ingredients_new = get_ingredients(request)
        for title, quantity in ingredients_new.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            amount = Amount(recipe=change_recipe,
                            ingredient=ingredient,
                            quantity=quantity)
            amount.save()
        form.save_m2m()
        return redirect('recipe', recipe_id=recipe.id)

    form = RecipeForm(instance=recipe)
    context = {'form': form,
               'recipe': recipe,
               'new': False,
               'image_name': recipe.image.name.split('/')[1]}
    return render(request, 'new_recipe.html', context)


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user == recipe.author:
        recipe.delete()
        return redirect('profile', username=request.user)
    return redirect('recipe', recipe_id=recipe_id)


@login_required
def favorites(request):
    tags_list = request.GET.getlist('tags')

    if not tags_list:
        tags_list = ['breakfast', 'lunch', 'dinner']

    all_tags = Tag.objects.all()

    recipe_list = Recipe.objects.filter(
        favorite_recipes__user=request.user
    ).filter(
        tags__value__in=tags_list
    ).distinct()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page': page,
        'all_tags': all_tags,
        'tags_list': tags_list
    }
    return render(request, 'my_favorite.html', context)


@login_required
def my_follow(request):
    subscriptions = User.objects.filter(
        following__user=request.user
    ).annotate(
        recipe_count=Count(
            'recipes'
        )
    )
    recipe = {}

    for sub in subscriptions:
        recipe[sub] = Recipe.objects.filter(
            author=sub
        )[:3]

    paginator = Paginator(subscriptions, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page': page,
        'recipe': recipe
    }
    return render(request, 'my_follow.html', context)


@login_required
def shop_list(request):
    if request.GET:
        recipe_id = request.GET.get('recipe_id')
        ShopList.objects.get(recipe__id=recipe_id).delete()
    purchases = Recipe.objects.filter(shop_list__user=request.user)
    context = {'purchases': purchases}
    return render(request, 'shop_list.html', context)


@login_required
def get_purchases(request):
    recipes = Recipe.objects.filter(shop_list__user=request.user)
    ing = {}
    for recipe in recipes:
        ingredients = recipe.ingredients.values_list('title', 'dimension')
        amount = recipe.recipe_amount.values_list('quantity', flat=True)
        for num in range(len(ingredients)):
            title = ingredients[num][0]
            dimension = ingredients[num][1]
            quantity = amount[num]
            if title in ing.keys():
                ing[title] = [ing[title][0] + quantity, dimension]
            else:
                ing[title] = [quantity, dimension]
    response = HttpResponse(content_type='txt/csv')
    response['Content-Disposition'] = 'attachment; filename=shop_list.txt"'
    writer = csv.writer(response)
    for key, value in ing.items():
        writer.writerow([f'{key} ({value[1]}) - {value[0]}'])
    return response


@login_required
@require_http_methods(['POST', 'DELETE'])
def change_favorites(request, recipe_id):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        obj, created = Favorite.objects.get_or_create(user=request.user,
                                                      recipe=recipe)
        if not created:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        removed = Favorite.objects.filter(user=request.user,
                                          recipe=recipe).delete()
        if removed:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


@login_required
@require_http_methods(['POST', 'DELETE'])
def purchases(request, recipe_id):
    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        obj, created = ShopList.objects.get_or_create(user=request.user,
                                                      recipe=recipe)
        if not created:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        removed = ShopList.objects.filter(user=request.user,
                                          recipe=recipe).delete()
        if removed:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


@login_required
@require_http_methods(['POST', 'DELETE'])
def subscriptions(request, author_id):
    if request.method == 'POST':
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)
        obj, created = Subscription.objects.get_or_create(user=request.user,
                                                          author=author)
        if request.user == author or not created:
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})
    elif request.method == 'DELETE':
        author = get_object_or_404(User, id=author_id)
        removed = Subscription.objects.filter(user=request.user,
                                              author=author).delete()
        if removed:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


def page_not_found(request, exception):
    return render(request, '404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, '500.html', status=500)
