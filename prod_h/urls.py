from django.urls import path

from . import views

urlpatterns = [
    path('recipes/<int:recipe_id>/', views.recipe_detail,
         name='recipe_detail'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('<str:username>/', views.authors_recipes, name='authors-recipes'),
    #path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('', views.index, name='index')
]