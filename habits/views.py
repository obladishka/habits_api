from rest_framework import generics

from habits.models import Habit
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializer, PublicHabitSerializer
from habits.services import create_replacements, create_schedule, create_task, make_replacements
from users.permissions import IsUser


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        if not habit.is_pleasant:
            replacements = create_replacements(habit)
            habit.frequency = make_replacements(habit.frequency, replacements)
            habit.save()
            print(habit.user.tg_chat_id)

            if habit.user.tg_chat_id:
                schedule = create_schedule(habit.frequency)
                create_task(schedule, habit)


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = PublicHabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsUser,)


class HabitUpdateAPIView(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsUser,)

    def perform_update(self, serializer):
        habit = serializer.save(user=self.request.user)
        habit.save()
        if not habit.is_pleasant:
            replacements = create_replacements(habit)
            habit.frequency = make_replacements(habit.frequency, replacements)
            habit.save()


class HabitDestroyAPIView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = (IsUser,)
