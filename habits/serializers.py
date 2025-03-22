from rest_framework import serializers

from config.settings import WEEKDAYS
from habits.models import Habit
from habits.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    end_time = serializers.DateTimeField(
        required=False, verbose_name="end time", help_text="Enter the last time for habit performance."
    )
    weekdays = serializers.MultipleChoiceField(
        choices=WEEKDAYS,
        required=False,
        verbose_name="weekdays",
        help_text="Select days when a habit should be performed.",
    )

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [HabitValidator()]

    def validate_time_needed(self, value):
        """Validates that time needed to perform a habit is less than 2 mins (120 secs)."""
        if value > 120:
            raise serializers.ValidationError("The time should be less then 2 mins (120 secs).")
        return value

    def validate_related_habit(self, value):
        """Validates that only a pleasant habit can be selected as related."""
        if not value.is_pleasant:
            raise serializers.ValidationError("Only a pleasant habit can be selected as related.")
        return value
