import csv
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .form import RecipeForm
from .maintenance import get_ingredients, get_tags_for_edit
from .models import (Amount, Favorite, Ingredient, Recipe, ShopList,
                     Subscription, Tag, User)


def index(request):
    tags_list = request.GET.getlist('filters')

    if not tags_list:
        tags_list = ['breakfast', 'lunch', 'dinner']

    recipe_list = Recipe.objects.filter(
        tags__value__in=tags_list
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()

    all_tags = Tag.objects.all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'paginator': paginator,
               'page': page,
               'all_tags': all_tags,
               'tags_list': tags_list}
    return render(request, 'index.html', context)


def profile_view(request, username):
    tags_list = request.GET.getlist('filters')

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
    text = request.GET['query']
    ingredients_list = Ingredient.objects.filter(title__istartswith=text)
    ing_list = []
    for ing in ingredients_list:
        ingredient_dict = dict()
        ingredient_dict['title'] = ing.title
        ingredient_dict['dimension'] = ing.dimension
        ing_list.append(ingredient_dict)
    return JsonResponse(ing_list, safe=False)


@login_required()
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    all_tags = Tag.objects.all()
    tags_post = get_tags_for_edit(request)
    new = True
    if not form.is_valid():
        context = {'form': form, 'all_tags': all_tags, 'new': new}
        return render(request, 'new_recipe.html', context)
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    ingredients = get_ingredients(request)
    for title, quantity in ingredients.items():
        ingredient = Ingredient.objects.get(title=title)
        ingredient_item = Amount(
            recipe=recipe,
            quantity=quantity,
            ingredient=ingredient
        )
        ingredient_item.save()
    for i in tags_post:
        tag = get_object_or_404(Tag, id=i)
        recipe.tags.add(tag)
    form.save_m2m()
    return redirect('index')


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    all_tags = Tag.objects.all()
    image_name = recipe.image.name.split('/')[1]
    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe_id)

    form = RecipeForm(
        request.POST,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        my_recipe = form.save(commit=False)
        my_recipe.author = request.user
        my_recipe.save()
        new_tags = get_tags_for_edit(request)
        my_recipe.recipe_amount.all().delete()
        ingredients = get_ingredients(request)
        for title, quantity in ingredients.items():
            ingredient = get_object_or_404(Ingredient, title=title)
            amount = Amount(
                recipe=my_recipe,
                ingredient=ingredient,
                quantity=quantity
            )
            amount.save()
        my_recipe.tags.set(new_tags)
        return redirect('recipe', recipe_id=recipe.id)
    form = RecipeForm(instance=recipe)
    context = {
        'form': form,
        'recipe': recipe,
        'all_tags': all_tags,
        'image_name': image_name
    }
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
    tags_list = request.GET.getlist('filters')
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
    response['Content-Disposition'] = 'attachment; filename="shop_list.txt"'
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
