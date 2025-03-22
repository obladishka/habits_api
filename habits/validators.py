from rest_framework import serializers


class HabitValidator:
    """Class for cross-filed validation logic."""

    def validate_reward(self, attrs):
        """Validates that only reward or a related habit are selected in the same time."""
        if attrs["related_habit"] and attrs["reward"]:
            raise serializers.ValidationError(
                "Related habit and reward can't be selected together. Select 1 of 2 options."
            )

    def validate_pleasant_habit(self, attrs):
        """Validates that a pleasant habit doesn't additionally have reward or related habit."""
        if attrs["is_pleasant"] and any([attrs["related_habit"], attrs["reward"]]):
            raise serializers.ValidationError(
                "Pleasant habit is already reward, it can't have a related habit or reward."
            )
        if not attrs["is_pleasant"] and not any([attrs["related_habit"], attrs["reward"]]):
            raise serializers.ValidationError("Good habit should have a reward or a related habit.")

    def validate_end_time(self, attrs):
        """Validates that a habit that should be performed several times per day has end time
        and this time is correct."""
        if "x" in attrs["frequency"] and not attrs["end_time"]:
            raise serializers.ValidationError(
                "For a habit that should be performed several times per day end time should be specified."
            )
        if "x" not in attrs["frequency"] and attrs["end_time"]:
            raise serializers.ValidationError(
                "End time should be only selected for habits performed several times per day."
            )
        if attrs["end_time"] > attrs["time"]:
            raise serializers.ValidationError("End time can't be earlier than start time")

    def validate_weekdays(self, attrs):
        """Validates selection of specific days of week when a habit should be performed."""
        if "d" in attrs["frequency"] and not attrs["weekdays"]:
            raise serializers.ValidationError(
                "For a habit that should be performed on specific days of week such days should be selected."
            )
        if "d" not in attrs["frequency"] and attrs["weekdays"]:
            raise serializers.ValidationError(
                "Specific days should be selected only for habits performed on selected days."
            )

    def __call__(self, attrs, serializer):
        self.validate_reward(attrs)
        self.validate_pleasant_habit(attrs)
        self.validate_end_time(attrs)
        self.validate_weekdays(attrs)
