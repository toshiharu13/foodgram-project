# Generated by Django 3.2.3 on 2021-06-02 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod_h', '0002_auto_20210602_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingridient',
            name='counts',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.DurationField(),
        ),
    ]
