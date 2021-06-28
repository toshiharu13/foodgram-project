from django import template

register = template.Library()


@register.filter
def follow_count(count):
    count = count - 3
    if count % 10 == 1 and count % 100 != 11:
        return f'Еще {str(count)} рецепт...'
    elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
        return f'Еще {str(count)} рецепта...'
    else:
        return f'Еще {str(count)} рецептов...'


@register.filter
def purchases_count(user):
    card_data = user.purchases.all().count()
    if card_data == 0:
        return ''
    return card_data


@register.filter
def bought_to(user, recipe):
    return user.purchases.filter(item=recipe).exists()


@register.filter
def fav_to(user, recipe):
    return user.favorites.filter(recipe=recipe).exists()


@register.filter
def foll_to(user, recipe):
    return user.follower.filter(user=user, author=recipe.author).exists()


@register.filter
def create_or_change(edit):
    if edit:
        return 'Редактирование рецепта'
    else:
        return 'Создание Рецепта'
