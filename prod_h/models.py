from datetime import datetime
from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model
from prod_h.serices import translate_rus_eng

User = get_user_model()

class ListOfIngridients(models.Model):
    # Таблица компонентов
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Название ингредиента',
                            help_text='Название ингредиента, максимум 50 символов',
                            )
    units_of_measurement = models.CharField(max_length=20,
                                            verbose_name='Единица измерения',
                                            help_text='Единица измерения, максимум 20 симоволов',
                                            )

    def __str__(self):
        return f'{self.name} ({self.units_of_measurement})'

class Teg(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор рецепта',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название рецепта',
        help_text='Максимальная длинна 100 символов',)
    image = models.ImageField(upload_to='prod_h/', blank=True, null=True)
    text = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Описание рецепта',)
    ingredients = models.ManyToManyField(
        ListOfIngridients,
        through='Amount',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Игредиенты',
        help_text='Игредиенты',)
    tags = models.ManyToManyField(Teg, )
    time = models.IntegerField(verbose_name='Вермя приготовления')
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    slug = models.SlugField(
        max_length=500,
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = translate_rus_eng(self.name) + '_' + datetime.strftime(
                timezone.now(), '%d_%m_%y_%H_%M_%S_%s'
            )
        super().save(*args, **kwargs)


    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
    )

class Amount(models.Model):
    ingredient = models.ForeignKey(ListOfIngridients,
                                   on_delete=models.CASCADE,
                                   related_name='ingridient_name', )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="recipe_ingredients",
        verbose_name='Рецепт',
    )
    counts = models.PositiveSmallIntegerField(verbose_name='количество',
        default=1)

    def __str__(self):
        return self.ingredient.name

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscription')
            ]
        verbose_name_plural = "Подписка"

class Cart(models.Model):
    item = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item', 'customer'],
                                    name='unique_purchase')
        ]
        verbose_name_plural = "Корзина"


