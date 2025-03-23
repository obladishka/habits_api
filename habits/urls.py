from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path("habits/new", HabitCreateAPIView.as_view(), name="habit-create"),
    # path("lessons", LessonListAPIView.as_view(), name="lesson_list"),
    # path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    # path("lessons/<int:pk>/update", LessonUpdateAPIView.as_view(), name="update_lesson"),
    # path("lessons/<int:pk>/delete", LessonDestroyAPIView.as_view(), name="delete_lesson"),
]
