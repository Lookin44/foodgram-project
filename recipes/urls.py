from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('<str:username>', views.profile, name='profile'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('follow/', views.follow, name='follow'),
    path('favorite/', views.favorite, name='favorite'),
    path('shop_list/', views.shop_list, name='shop_list'),
]
