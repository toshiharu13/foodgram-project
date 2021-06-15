from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ListOfIngridients(models.Model):
    name = models.CharField(max_length=50)
    units_of_measurement = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Teg(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Ingridient(models.Model):
    name = models.ForeignKey(ListOfIngridients,
                             on_delete=models.CASCADE,
                             related_name='ingridient_name',)
    units_of_measurement = models.ManyToManyField(ListOfIngridients,)
    counts = models.PositiveSmallIntegerField(verbose_name='количество',
        default=1)

    def __str__(self):
        return self.name.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='authors recipe',
    )
    name = models.CharField(verbose_name='recipe name', max_length=50)
    image = models.ImageField(upload_to='prod_h/', blank=True, null=True)
    text = models.TextField(verbose_name='recipe description')
    ingridients = models.ManyToManyField(Ingridient,)
    teg = models.ManyToManyField(Teg,)
    time = models.IntegerField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:15]



