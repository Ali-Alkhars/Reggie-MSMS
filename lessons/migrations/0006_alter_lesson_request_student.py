# Generated by Django 4.1.3 on 2022-11-28 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0005_lesson_request_student_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson_request",
            name="student",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
