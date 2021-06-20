from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('change_favorites/<int:recipe_id>/', views.change_favorites,
         name='change_favorites'),
    path('favorites/', views.favorites, name='favorites'),
    path('follow/', views.my_follow, name='follow'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('new_recipe/', views.new_recipe, name='new_recipe'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('purchases/', views.get_purchases, name='get_purchases'),
    path('purchases/<int:recipe_id>/', views.purchases, name='purchases'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete,
         name='recipe_delete'),
    path('subscriptions/<int:author_id>/', views.subscriptions,
         name='subscriptions'),
    path('shop_list/', views.shop_list, name='shop_list'),
]
