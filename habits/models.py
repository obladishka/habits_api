from django.db import models

from config.settings import HABIT_FREQUENCY
from users.models import User


class Week(models.Model):
    """Model for storaging days of week."""

    day = models.CharField(max_length=3, verbose_name="day of week")


class Habit(models.Model):

    user = models.ForeignKey(
        User, verbose_name="user", on_delete=models.CASCADE, related_name="habits", null=True, blank=True
    )
    place = models.CharField(
        max_length=200, verbose_name="place", help_text="Enter the place where you'll perform your habit."
    )
    time = models.DateTimeField(
        verbose_name="time",
        help_text="Enter the time when a habit should be performed. In case a habit should be performed several times "
        "per day, the end time should also be selected. For good habits only!",
        null=True,
        blank=True,
    )
    action = models.CharField(max_length=200, verbose_name="action", help_text="Enter the action to perform.")
    is_pleasant = models.BooleanField(
        verbose_name="pleasant or not",
        help_text="Select whether a habit is pleasant or not. "
        "Only pleasant habits can serve as rewards for good habits.",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="related habit",
        help_text="Select a related pleasant habit (as a reward). For good habits only!",
        blank=True,
        null=True,
    )
    frequency = models.CharField(
        choices=HABIT_FREQUENCY,
        verbose_name="frequency",
        help_text="Select how often a good habit should be performed. "
        "NOTE! A good habit should be performed once a week at least. For good habits only!",
        default="m h * * *",
        blank=True,
        null=True,
    )
    reward = models.CharField(
        max_length=200,
        verbose_name="reward",
        help_text="Enter the reward for habit performance.",
        blank=True,
        null=True,
    )
    end_time = models.DateTimeField(
        verbose_name="end time",
        help_text="Enter the time when a habit should be performed for the last time per day. "
        "Only for good habits that should be performed several times per day!",
        null=True,
        blank=True,
    )
    days_of_week = models.ManyToManyField(
        Week,
        verbose_name="day(s) of week",
        help_text="Select specific days when a good habit should be performed.",
        null=True,
        blank=True,
    )
    time_needed = models.PositiveIntegerField(
        verbose_name="time needed",
        help_text="Enter time needed to perform a habit in secs. Not more than 2 mins (120 sec).",
    )
    is_public = models.BooleanField(
        verbose_name="public or not", help_text="Select whether you want other users see your habit."
    )
