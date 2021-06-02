from django.contrib import admin

from .models import Tag, Ingredient, Recipe, Follow, Favorites


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit')
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'slug')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
