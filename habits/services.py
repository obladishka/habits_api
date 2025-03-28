from datetime import datetime

from habits.models import Habit


def create_replacements(habit: Habit) -> dict[str, str | list[str]]:
    """Renders a dict of replacements."""
    m = datetime.fromisoformat(habit.time).time().minute
    h = x = datetime.fromisoformat(habit.time).time().hour
    y = datetime.fromisoformat(habit.end_time).time().hour if habit.end_time else 0
    z = (x + y) // 2
    d = ",".join([day.day for day in habit.days_of_week.all()]) if habit.days_of_week else "d"
    return {"m": str(m), "x": str(x), "y": str(y), "z": str(z), "h": str(h), "d": d}


def make_replacements(text: str, replacements: dict) -> str:
    """Replaces vars in text with correct values."""
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text
