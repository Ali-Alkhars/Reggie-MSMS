# Generated by Django 4.1.3 on 2022-11-21 21:19

from django.db import migrations, models
import lessons.models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0002_lesson_request_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson_request",
            name="AdditionalNotes",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="lesson_request",
            name="DurationOfLesson",
            field=models.PositiveIntegerField(
                validators=[lessons.models.validate_nonzero]
            ),
        ),
        migrations.AlterField(
            model_name="lesson_request",
            name="IntervalBetweenLessons",
            field=models.PositiveIntegerField(
                validators=[lessons.models.validate_nonzero]
            ),
        ),
        migrations.AlterField(
            model_name="lesson_request",
            name="LearningObjectives",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="lesson_request",
            name="availableDays",
            field=models.CharField(
                choices=[
                    ("Monday", "Monday"),
                    ("Tuesday", "Tuesday"),
                    ("Wednesday", "Wednesday"),
                    ("Thursday", "Thursday"),
                    ("Friday", "Friday"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="lesson_request",
            name="availableTimes",
            field=models.CharField(
                choices=[
                    ("Morning", "Morning"),
                    ("Afternoon", "Afternoon"),
                    ("Night", "Night"),
                ],
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="lesson_request",
            name="numberOfLessons",
            field=models.PositiveIntegerField(
                validators=[lessons.models.validate_nonzero]
            ),
        ),
    ]
