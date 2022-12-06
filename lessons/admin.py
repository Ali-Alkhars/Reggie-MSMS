"""Configuration of the admin interface for MSMS"""
from django.contrib import admin
from .models import Lesson_request
from lessons.models import User

# Register your models here.
@admin.register(Lesson_request)
class LessonAdmin(admin.ModelAdmin):
    lesson_attribute = [
        "availableDays",
        "availableTimes",
        "numberOfLessons",
        "IntervalBetweenLessons",
        "DurationOfLesson",
        "LearningObjectives",
        "AdditionalNotes",
    ]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'username', 'first_name', 'last_name', 'is_active',
    ]
