
from django import template

register = template.Library()

@register.filter
def follow_count(count):
    count = count - 3
    if count % 10 == 1 and count % 100 != 11:
        return f"Еще {str(count)} рецепт..."
    elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
        return f"Еще {str(count)} рецепта..."
    else:
        return f"Еще {str(count)} рецептов..."