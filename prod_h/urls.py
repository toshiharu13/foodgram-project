from django.urls import path

from . import views

urlpatterns = [
    path('recipes/<int:recipe_id>/', views.recipe_detail,
         name='recipe_detail'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('following/', views.follow_index, name='follow'),
    path('my_favorite/', views.favorite_index, name='my_favorite'),
    path('<str:username>/', views.authors_recipes, name='authors-recipes'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:recipe_id>/', views.remove_recipe_from_cart,
         name='remove_recipe_from_cart'),
    path('download/', views.download, name='download'),

    path('', views.index, name='index'),
    path('<str:username>/follow/', views.profile_follow,
         name='profile_follow'),
    path('<str:username>/unfollow/', views.profile_unfollow,
        name='profile_unfollow'),
]