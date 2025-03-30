import requests
from celery import shared_task

from config.settings import TELEGRAM_BOT_TOKEN
from habits.models import Habit


@shared_task
def send_message(pk) -> None:
    """Sends reminders to user's telegram."""
    habit = Habit.objects.get(pk=pk)
    text = (
        f"It's time to do {habit.action} at {habit.place}! "
        f"Don't forget to {habit.reward if habit.reward else habit.related_habit} afterwards."
    )
    params = {
        "text": text,
        "chat_id": habit.user.tg_chat_id,
    }
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
