# Generated by Django 5.0.4 on 2024-04-30 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_alter_category_options_alter_offer_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_en', models.CharField(max_length=255, verbose_name='Колір англійською')),
                ('color_ua', models.CharField(max_length=255, verbose_name='Колір українською')),
                ('color_ru', models.CharField(max_length=255, verbose_name='Колір російською')),
            ],
            options={
                'verbose_name_plural': 'Кольори',
            },
        ),
    ]
