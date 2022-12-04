# Generated by Django 4.1.3 on 2022-12-03 15:34

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0003_alter_invoice_creation_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="creation_date",
            field=models.DateTimeField(
                validators=[
                    django.core.validators.MaxValueValidator(
                        limit_value=datetime.datetime.today
                    )
                ]
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="update_date",
            field=models.DateTimeField(
                validators=[
                    django.core.validators.MaxValueValidator(
                        limit_value=datetime.datetime.today
                    )
                ]
            ),
        ),
    ]