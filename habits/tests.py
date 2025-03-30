from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, Week
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@user.ru")
        self.good_habit = Habit.objects.create(
            user=self.user,
            place="Place 1",
            time="2025-03-30T15:30:00+03:00",
            action="Action 1",
            is_pleasant=False,
            frequency="30 15 * * *",
            reward="Reward 1",
            time_needed=90,
            is_public=True,
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Pleasant place 1",
            action="Pleasant action 1",
            is_pleasant=True,
            time_needed=30,
            is_public=False,
        )
        self.user2 = User.objects.create(email="user2@user.ru")
        self.pleasant_habit2 = Habit.objects.create(
            user=self.user2,
            place="Pleasant place 2",
            action="Pleasant action 2",
            is_pleasant=True,
            time_needed=30,
            is_public=True,
        )
        self.pleasant_habit3 = Habit.objects.create(
            user=self.user2,
            place="Pleasant place 3",
            action="Pleasant action 3",
            is_pleasant=True,
            time_needed=30,
            is_public=False,
        )
        self.mon = Week.objects.create(day="mon")
        self.tue = Week.objects.create(day="tue")
        self.client.force_authenticate(user=self.user)

    def test_habit_create_good_habit(self):
        url = reverse("habits:habit-create")
        body = {
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "frequency": "m h * * *",
            "reward": "Reward 2",
            "time_needed": 90,
            "is_public": False,
        }
        request = self.client.post(url, body)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 5)
        frequency = Habit.objects.get(place="Place 2").frequency
        self.assertEqual(frequency, "30 16 * * *")

    # def test_lesson_create_error(self):
    #     url = reverse("courses:create_lesson")
    #     body = {"name": "My Lesson", "video_url": "https://my.sky.pro"}
    #     request = self.client.post(url, body)
    #     response = request.json()
    #
    #     self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.get("video_url"), ["Link for third-party resources are not allowed."])
    #
    # def test_lesson_retrieve(self):
    #     url = reverse("courses:lesson_detail", args=(self.lesson.pk,))
    #     request = self.client.get(url)
    #     response = request.json()
    #
    #     self.assertEqual(request.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.get("name"), "Lesson 1")
    #     self.assertEqual(response.get("owner"), self.user.pk)
    #
    # def test_lesson_retrieve_error(self):
    #     url = reverse("courses:lesson_detail", args=(self.lesson2.pk,))
    #     request = self.client.get(url)
    #     response = request.json()
    #
    #     self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(response.get("detail"), "You do not have permission to perform this action.")
    #
    # def test_lesson_list(self):
    #     url = reverse("courses:lesson_list")
    #     request = self.client.get(url)
    #     response = request.json()
    #
    #     self.assertEqual(request.status_code, status.HTTP_200_OK)
    #     self.assertEqual(
    #         response,
    #         {
    #             "count": 1,
    #             "next": None,
    #             "previous": None,
    #             "results": [
    #                 {
    #                     "id": self.lesson.pk,
    #                     "video_url": None,
    #                     "name": self.lesson.name,
    #                     "description": None,
    #                     "preview": None,
    #                     "course": None,
    #                     "owner": self.user.pk,
    #                 }
    #             ],
    #         },
    #     )
    #
    # def test_lesson_update(self):
    #     url = reverse("courses:update_lesson", args=(self.lesson.pk,))
    #     body = {"name": "My Lesson"}
    #     request = self.client.patch(url, body)
    #     response = request.json()
    #
    #     self.assertEqual(request.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.get("name"), "My Lesson")
    #
    # def test_lesson_delete(self):
    #     url = reverse("courses:delete_lesson", args=(self.lesson.pk,))
    #     request = self.client.delete(url)
    #
    #     self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Lesson.objects.all().count(), 1)
