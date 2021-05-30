from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Recipe


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
    context = {'recipe': recipe,
               'author': recipe.author,
               }
    return render(request, 'recipe_main.html', context)
