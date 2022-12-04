# Generated by Django 4.1.3 on 2022-12-03 15:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="price",
            field=models.FloatField(
                validators=[django.core.validators.MaxValueValidator(1000000)]
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="unpaid",
            field=models.FloatField(
                validators=[django.core.validators.MaxValueValidator(1000000)]
            ),
        ),
    ]
