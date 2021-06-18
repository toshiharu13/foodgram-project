from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse

from prod_h.utils import get_tags, get_ingredients, tags_filter
from prod_h.models import Recipe, User, Teg
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required


def index(request):
    tags = tags_filter(request)
    latest = Recipe.objects.filter(tags__name__in=tags).prefetch_related('tags').select_related('author').distinct()
    paginator = Paginator(latest, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_tags = Teg.objects.all()
    context = {
        "posts": latest,
        "page": page,
        'paginator': paginator,
        'all_tags': all_tags,
    }
    return render(request, "indexNotAuth.html", context=context)

def authors_recipes(request, username):
    author = get_object_or_404(User, username=username)
    user_recipe = author.recipes.all()
    paginator = Paginator(user_recipe, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'author': author,}
    return render(request, "authorRecipe.html", context=context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {
        'recipe': recipe,
    }
    return render(request, 'singlePage.html', context=context)

@login_required
def new_recipe(request):
    '''if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('index')

        return render(request, 'formRecipe.html', {'form': form})
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})'''


    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      initial={'author': request.user})
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        form.save()
        # Adds tags to the recipe
        for name_tag in get_tags(request):
            tag_from_bd = get_object_or_404(Teg, name=name_tag)
            instance.tags.add(tag_from_bd.id)
        # Adds ingredients to the recipe
        list_of_ingredients = get_ingredients(request, instance)
        for ingr in list_of_ingredients:
            instance.ingredients.add(ingr)

        return redirect('index')
    return render(request, 'formRecipe.html', {'form': form})