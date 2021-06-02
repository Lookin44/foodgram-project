from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Recipe, Ingredient, Tag
from .form import RecipeForm
from users.models import User


def index(request):
    recipes_list = Recipe.objects.all()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page,
               'paginator': paginator}
    return render(request, 'index.html', context)


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {'recipe': recipe}
    return render(request, 'recipe_main.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes_list = author.recipes.all()
    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page,
               'paginator': paginator,
               'author': author}
    return render(request, 'profile.html', context)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        return redirect('index')
    return render(request, 'new_recipe.html', {'form': form})


@login_required
def follow(request):
    subscription = Recipe.objects.filter(author__following__user=request.user)
    paginator = Paginator(subscription, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page,
               'paginator': paginator,
               'subscription': subscription}
    return render(request, 'my_follow.html', context)


@login_required
def favorite(request):
    favorite_list = Recipe.objects.filter(author__following__user=request.user)
    paginator = Paginator(favorite_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page,
               'paginator': paginator}
    return render(request, 'my_favorite.html', context)


def shop_list(request):
    recipes_list = Recipe.objects.all()
    context = {'recipes_list': recipes_list}
    return render(request, 'shop_list.html', context)
