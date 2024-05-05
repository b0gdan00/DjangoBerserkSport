# Generated by Django 5.0.4 on 2024-05-04 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='images',
            field=models.ManyToManyField(to='Main.image', verbose_name='Зображення'),
        ),
        migrations.AddField(
            model_name='offer',
            name='parameters',
            field=models.ManyToManyField(to='Main.parametr', verbose_name='Параметри'),
        ),
    ]