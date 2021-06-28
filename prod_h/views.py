import datetime as dt

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from prod_h.models import Amount, Cart, Follow, Recipe, Teg, User
from prod_h.utils import download_pdf, get_ingredients, get_tags, tags_filter

from .forms import RecipeForm


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
    all_tags = Teg.objects.all()
    context = {
        'page': page,
        'paginator': paginator,
        'author': author,
        'all_tags': all_tags,
    }
    return render(request, "authorRecipe.html", context=context)


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {
        'recipe': recipe,
    }
    return render(request, 'singlePage.html', context=context)


@login_required
def new_recipe(request):
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


@login_required
def recipe_edit(request, recipe_id):
    # Edit instance
    edit = True
    instance = get_object_or_404(Recipe, id=recipe_id)
    if not request.user.is_superuser:
        if instance.author != request.user:
            return redirect('recipe_detail', instance.id)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=instance)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.tags.clear()
        recipe.save()
        # Adds tags to the recipe
        for name_tag in get_tags(request):
            tag = get_object_or_404(Teg, name=name_tag)
            recipe.tags.add(tag.id)

        Amount.objects.filter(recipe=recipe).delete()
        # Adds ingredients to the recipe
        list_of_ingredients = get_ingredients(request, recipe)
        for ingr in list_of_ingredients:
            recipe.ingredients.add(ingr)
        return redirect('index')
    context = {
        'edit': edit,
        'recipe': instance,
        'form': form,
        'tags': instance.tags.all()
    }
    return render(request, 'formRecipe.html', context)


def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if not request.user.is_superuser:
        if request.user != recipe.author:
            return redirect('recipe_detail', recipe.id)

    recipe.delete()
    return redirect('authors-recipes', request.user.username)


@login_required
def follow_index(request):
    # The subscriber page is displayed.
    author_list = request.user.follower.all()

    paginator = Paginator(author_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        "paginator": paginator
    }
    return render(request, 'myFollow.html', context)


@login_required
def favorite_index(request):
    # The favorite recipe page is displayed.
    tags = tags_filter(request)
    recipe_list = Recipe.objects.filter(
        favorite__user=request.user,
        tags__name__in=tags
    ).prefetch_related('tags').select_related('author').distinct()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': tags,
        'all_tags': Teg.objects.all(),
        'page': page,
        "paginator": paginator
    }
    return render(request, 'favorite.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author == request.user:
        return redirect('follow')
    Follow.objects.get_or_create(
        author=get_object_or_404(User, username=username),
        user=request.user,
    )
    return redirect('follow')


@login_required
def profile_unfollow(request, username):
    Follow.objects.filter(
        author=get_object_or_404(User, username=username),
        user=request.user,
    ).delete()
    return redirect('follow')


@login_required
def cart(request):
    # Site cart.
    context = {
        'recipes': request.user.purchases.all(),
    }
    return render(request, 'shopList.html', context)


def remove_recipe_from_cart(request, recipe_id):
    # Removes selected recipes from the cart.
    recipes = get_object_or_404(Recipe, id=recipe_id)
    Cart.objects.filter(item=recipes, customer=request.user).delete()
    return redirect('cart')


def download(request):
    # The request loads the ingredients of the selected recipes.
    # And their amount.
    data_not_sum = request.user.purchases.all().select_related(
            'item'
        ).order_by(
            'item__ingredients__name'
        ).values(
            'item__ingredients__name',
        'item__ingredients__units_of_measurement')
    data = data_not_sum.annotate(
        amount=Sum('item__recipe_ingredients__counts')).all()
    return download_pdf(data)
