# Generated by Django 5.0.6 on 2024-05-17 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_remove_offer_parameters_delete_parametr'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='catCodeEpic',
            field=models.IntegerField(blank=True, null=True, verbose_name='Epic Code'),
        ),
    ]
