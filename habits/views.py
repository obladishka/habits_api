from rest_framework import generics

from habits.serializers import HabitSerializer
from habits.services import make_replacements


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        if not habit.is_pleasant:
            m = habit.time.time().minute
            h = x = habit.time.time().hour
            y = habit.end_time.time().hour if habit.end_time else "0"
            z = (x + y) // 2
            d = ",".join([day.day for day in habit.days_of_week.all()]) if habit.days_of_week else "d"
            replacements = {"m": str(m), "x": str(x), "y": str(y), "z": str(z), "h": str(h), "d": d}
            habit.frequency = make_replacements(habit.frequency, replacements)
            habit.save()
        habit.save()
