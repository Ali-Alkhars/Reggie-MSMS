from django.contrib import admin
from .models import Lesson_request

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