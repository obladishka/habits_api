from datetime import datetime

from rest_framework import serializers

from habits.models import Habit


class HabitValidator:
    def validate_time_needed(self, attrs):
        """Validates that time needed to perform a habit is less than 2 mins (120 secs)."""
        if attrs["time_needed"] > 120:
            raise serializers.ValidationError("The time should be less then 2 mins (120 secs).")

    def validate_related_habit(self, attrs):
        """Validates that only a pleasant habit can be selected as related."""
        if attrs.get("related_habit_id"):
            related_habit = Habit.objects.get(pk=attrs.get("related_habit_id"))
            if not related_habit.is_pleasant:
                raise serializers.ValidationError("Only a pleasant habit can be selected as related.")

    def validate_reward(self, attrs):
        """Validates that only reward or a related habit are selected in the same time."""
        if attrs.get("related_habit_id") and attrs.get("reward"):
            raise serializers.ValidationError(
                "Related habit and reward can't be selected together. Select 1 of 2 options."
            )

    def validate_pleasant_habit(self, attrs):
        """Validates that a pleasant habit doesn't additionally have reward, related habit,
        time and frequency to be performed."""
        if attrs.get("is_pleasant") and any(
            [attrs.get("related_habit_id"), attrs.get("reward"), attrs.get("frequency"), attrs.get("time")]
        ):
            raise serializers.ValidationError(
                "Pleasant habit is already reward, it can't have a related habit or reward "
                "and should not be performed regularly."
            )
        if not attrs.get("is_pleasant") and not any(
            [
                all([attrs.get("reward"), attrs.get("frequency"), attrs.get("time")]),
                all([attrs.get("related_habit_id"), attrs.get("frequency"), attrs.get("time")]),
            ]
        ):
            raise serializers.ValidationError(
                "Good habit should have a reward or a related habit and should be performed regularly "
                "and on specific time."
            )

    def validate_end_time(self, attrs):
        """Validates that a habit that should be performed several times per day has end time
        and this time is correct."""
        if attrs.get("frequency") and "x" in attrs.get("frequency") and not attrs.get("end_time"):
            raise serializers.ValidationError(
                "For a habit that should be performed several times per day end time should be specified."
            )
        if attrs.get("frequency") and "x" not in attrs.get("frequency") and attrs.get("end_time"):
            raise serializers.ValidationError(
                "End time should be only selected for habits performed several times per day."
            )
        if (
            attrs.get("end_time")
            and attrs.get("time")
            and datetime.fromisoformat(attrs.get("end_time")).date()
            != datetime.fromisoformat(attrs.get("time")).date()
        ):
            raise serializers.ValidationError("Start and end time should be selected within 1 day.")
        if attrs.get("end_time") and attrs.get("time") and attrs.get("end_time") <= attrs.get("time"):
            raise serializers.ValidationError("End time can't be earlier than or equal to start time.")

    def validate_days_of_week(self, attrs):
        """Validates selection of specific days of week when a habit should be performed."""
        if attrs.get("frequency") and "d" in attrs.get("frequency") and not attrs.get("days_of_week"):
            raise serializers.ValidationError(
                "For a habit that should be performed on specific days of week such days should be selected."
            )
        if attrs.get("frequency") and "d" not in attrs.get("frequency") and attrs.get("days_of_week"):
            raise serializers.ValidationError(
                "Specific days should be selected only for habits performed on selected days."
            )

    def __call__(self, attrs):
        self.validate_time_needed(attrs)
        self.validate_related_habit(attrs)
        self.validate_reward(attrs)
        self.validate_pleasant_habit(attrs)
        self.validate_end_time(attrs)
        self.validate_days_of_week(attrs)
