from django.urls import path

from . import views

urlpatterns = [
    path('recipes/<int:recipe_id>/', views.recipe_detail,
         name='recipe_detail'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('<str:username>/', views.authors_recipes, name='authors-recipes'),
    #path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('', views.index, name='index')
]