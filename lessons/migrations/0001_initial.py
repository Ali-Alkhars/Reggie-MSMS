# Generated by Django 4.1.3 on 2022-12-06 13:41

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import lessons.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=80,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_username",
                                message="Username must be an Email",
                                regex="[a-z0-9]+@[a-z]+\\.[a-z]{2,3}",
                            )
                        ],
                    ),
                ),
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="TermTime",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("startDate", models.DateField(help_text="Enter a date after now")),
                (
                    "endDate",
                    models.DateField(
                        help_text="Enter a date after now and after start date"
                    ),
                ),
                ("midTerm", models.DateField()),
                (
                    "termOrder",
                    models.CharField(
                        choices=[
                            ("First term", "First term"),
                            ("Second term", "Second term"),
                        ],
                        default="First Term",
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lesson_request",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "availableDays",
                    models.CharField(
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
                (
                    "availableTimes",
                    models.CharField(
                        choices=[
                            ("Morning", "Morning"),
                            ("Afternoon", "Afternoon"),
                            ("Night", "Night"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "numberOfLessons",
                    models.PositiveIntegerField(
                        validators=[lessons.models.validate_nonzero]
                    ),
                ),
                (
                    "IntervalBetweenLessons",
                    models.PositiveIntegerField(
                        validators=[lessons.models.validate_nonzero]
                    ),
                ),
                (
                    "DurationOfLesson",
                    models.PositiveIntegerField(
                        choices=[
                            (15, "15 minutes"),
                            (30, "30 minutes"),
                            (45, "45 minutes"),
                            (60, "60 minutes"),
                            (75, "75 minutes"),
                            (90, "90 minutes"),
                            (105, "105 minutes"),
                            (120, "120 minutes"),
                        ],
                        validators=[lessons.models.validate_nonzero],
                    ),
                ),
                ("LearningObjectives", models.TextField()),
                ("AdditionalNotes", models.TextField(blank=True)),
                ("Fulfilled", models.CharField(default="Pending", max_length=50)),
                (
                    "student",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "reference",
                    models.CharField(
                        max_length=50,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_reference",
                                message="Reference number should be numbers-numbers",
                                regex="^[0-9-]*$",
                            )
                        ],
                    ),
                ),
                (
                    "price",
                    models.FloatField(
                        validators=[django.core.validators.MaxValueValidator(1000000)]
                    ),
                ),
                (
                    "unpaid",
                    models.FloatField(
                        validators=[django.core.validators.MaxValueValidator(1000000)]
                    ),
                ),
                (
                    "creation_date",
                    models.DateTimeField(
                        validators=[
                            django.core.validators.MaxValueValidator(
                                limit_value=django.utils.timezone.now
                            )
                        ]
                    ),
                ),
                (
                    "update_date",
                    models.DateTimeField(
                        validators=[
                            django.core.validators.MaxValueValidator(
                                limit_value=django.utils.timezone.now
                            )
                        ]
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
