from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import POSTS_COUNT
from prod_h.models import Amount, Cart, Follow, Recipe, Tag, User
from prod_h.utils import download_pdf, tags_filter

from .forms import RecipeForm
from .utils import check


def index(request):
    tags = tags_filter(request)
    latest = Recipe.objects.filter(
        tags__name__in=tags
    ).prefetch_related(
        'tags'
    ).select_related(
        'author'
    ).distinct()
    paginator = Paginator(latest, POSTS_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_tags = Tag.objects.all()
    context = {
        'posts': latest,
        'page': page,
        'paginator': paginator,
        'all_tags': all_tags,
        'tags_in_page': tags,
    }
    return render(request, 'indexNotAuth.html', context=context)


def authors_recipes(request, username):
    tags = tags_filter(request)
    author = get_object_or_404(User, username=username)
    user_recipe = Recipe.objects.filter(
        tags__name__in=tags,
        author=author,
    ).prefetch_related(
        'tags'
    ).select_related(
        'author'
    ).distinct()
    paginator = Paginator(user_recipe, POSTS_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    all_tags = Tag.objects.all()
    context = {
        'page': page,
        'paginator': paginator,
        'author': author,
        'all_tags': all_tags,
        'tags_in_page': tags,
    }
    return render(request, 'authorRecipe.html', context=context)


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
    if request.POST:
        check(request, form)
    if form.is_valid():
        form.save(request=request)
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
    if request.POST:
        check(request, form)
    if form.is_valid():
        instance.tags.clear()
        Amount.objects.filter(recipe=instance).delete()
        form.save(request=request)
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

    paginator = Paginator(author_list, POSTS_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator
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

    paginator = Paginator(recipe_list, POSTS_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'tags': tags,
        'all_tags': Tag.objects.all(),
        'page': page,
        'paginator': paginator
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
        'item').order_by('item__ingredients__name').values(
        'item__ingredients__name',
        'item__ingredients__units_of_measurement')
    data = data_not_sum.annotate(
        amount=Sum('item__recipe_ingredients__counts')).all()
    return download_pdf(data)
