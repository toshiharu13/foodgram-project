from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse

#from .models import Recipe, User
from prod_h.models import Recipe, User
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required


def index(request):
    latest = Recipe.objects.order_by('-pub_date')
    paginator = Paginator(latest, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "indexNotAuth.html",
        {"posts": latest, "page": page, 'paginator': paginator})

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
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('index')

        return render(request, 'formRecipe.html', {'form': form})
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form': form})