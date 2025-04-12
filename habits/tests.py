from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, Week
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@user.ru")
        self.good_habit = Habit.objects.create(
            pk=1,
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
            pk=2,
            user=self.user,
            place="Pleasant place 1",
            action="Pleasant action 1",
            is_pleasant=True,
            time_needed=30,
            is_public=False,
        )
        self.user2 = User.objects.create(email="user2@user.ru")
        self.pleasant_habit2 = Habit.objects.create(
            pk=3,
            user=self.user2,
            place="Pleasant place 2",
            action="Pleasant action 2",
            is_pleasant=True,
            time_needed=30,
            is_public=True,
        )
        self.pleasant_habit3 = Habit.objects.create(
            pk=4,
            user=self.user2,
            place="Pleasant place 3",
            action="Pleasant action 3",
            is_pleasant=True,
            time_needed=30,
            is_public=False,
        )
        self.mon = Week.objects.create(pk=1, day="mon")
        self.tue = Week.objects.create(pk=2, day="tue")
        self.client.force_authenticate(user=self.user)

    def test_habit_create_good_habit_with_reward(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "frequency": "m h * * d",
            "reward": "Reward 2",
            "time_needed": 90,
            "days_of_week": [1, 2],
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 5)
        frequency = Habit.objects.get(place="Place 2").frequency
        self.assertEqual(frequency, "30 16 * * mon,tue")

    def test_habit_create_good_habit_with_related_habit(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "frequency": "m h * * *",
            "related_habit_id": 2,
            "time_needed": 90,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 5)
        frequency = Habit.objects.get(place="Place 2").frequency
        self.assertEqual(frequency, "30 16 * * *")

    def test_habit_create_good_habit_time_needed_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "frequency": "m h * * *",
            "reward": "Reward 2",
            "time_needed": 125,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("non_field_errors"), ["The time should be less then 2 mins (120 secs)."])

    def test_habit_create_good_habit_related_habit_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "frequency": "m h * * *",
            "related_habit_id": 1,
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("non_field_errors"), ["Only a pleasant habit can be selected as related."])

    def test_habit_create_good_habit_reward_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "frequency": "m h * * *",
            "reward": "Reward 2",
            "related_habit_id": 2,
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["Related habit and reward can't be selected together. Select 1 of 2 options."],
        )

    def test_habit_create_good_habit_no_reward_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "frequency": "m h * * *",
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "Good habit should have a reward or a related habit and should be performed regularly "
                "and on specific time."
            ],
        )

    def test_habit_create_good_habit_no_time_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "action": "Action 2",
            "is_pleasant": False,
            "frequency": "m h * * *",
            "reward": "Reward 2",
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "Good habit should have a reward or a related habit and should be performed regularly "
                "and on specific time."
            ],
        )

    def test_habit_create_good_habit_no_frequency_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "reward": "Reward 2",
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "Good habit should have a reward or a related habit and should be performed regularly "
                "and on specific time."
            ],
        )

    def test_habit_create_good_no_end_time_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "reward": "Reward 2",
            "frequency": "m x-y * * *",
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["For a habit that should be performed several times per day end time should be specified."],
        )

    def test_habit_create_good_end_time_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "reward": "Reward 2",
            "frequency": "m h * * *",
            "end_time": "2025-03-30T18:30:00+03:00",
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["End time should be only selected for habits performed several times per day."],
        )

    def test_habit_create_good_end_time_and_start_time_not_in_the_same_day_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "reward": "Reward 2",
            "frequency": "m x-y * * *",
            "end_time": "2025-03-31T18:30:00+03:00",
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("non_field_errors"), ["Start and end time should be selected within 1 day."])

    def test_habit_create_good_end_time_earlier_than_start_time_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "reward": "Reward 2",
            "frequency": "m x-y * * *",
            "end_time": "2025-03-30T12:30:00+03:00",
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("non_field_errors"), ["End time can't be earlier than or equal to start time."])

    def test_habit_create_no_days_of_week_error_1(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "reward": "Reward 2",
            "frequency": "m h * * d",
            "time_needed": 120,
            "is_public": False,
            "days_of_week": [],
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["For a habit that should be performed on specific days of week such days should be selected."],
        )

    def test_habit_create_no_days_of_week_error_2(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "reward": "Reward 2",
            "frequency": "m h * * d",
            "time_needed": 120,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["For a habit that should be performed on specific days of week such days should be selected."],
        )

    def test_habit_create_no_days_of_week_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Place 2",
            "time": "2025-03-30T16:30:00+03:00",
            "action": "Action 2",
            "is_pleasant": False,
            "reward": "Reward 2",
            "frequency": "m x-y * * *",
            "end_time": "2025-03-30T17:30:00+03:00",
            "time_needed": 120,
            "is_public": False,
            "days_of_week": [1],
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            ["Specific days should be selected only for habits performed on selected days."],
        )

    def test_habit_create_pleasant_habit(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "is_pleasant": True,
            "time_needed": 90,
            "is_public": False,
        }
        request = self.client.post(url, body, format="json")

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 5)
        frequency = Habit.objects.get(place="Pleasant place new").frequency
        self.assertEqual(frequency, "m h * * *")

    def test_habit_create_pleasant_habit_related_habit_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "is_pleasant": True,
            "time_needed": 90,
            "is_public": False,
            "related_habit_id": 2,
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "Pleasant habit is already reward, it can't have a related habit or reward "
                "and should not be performed regularly."
            ],
        )

    def test_habit_create_pleasant_habit_reward_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "is_pleasant": True,
            "time_needed": 90,
            "is_public": False,
            "reward": "Pleasant reward new",
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "Pleasant habit is already reward, it can't have a related habit or reward "
                "and should not be performed regularly."
            ],
        )

    def test_habit_create_pleasant_habit_frequency_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "is_pleasant": True,
            "time_needed": 90,
            "is_public": False,
            "frequency": "m h */2 * *",
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "Pleasant habit is already reward, it can't have a related habit or reward "
                "and should not be performed regularly."
            ],
        )

    def test_habit_create_pleasant_habit_time_error(self):
        url = reverse("habits:habit-create")
        body = {
            "pk": 5,
            "place": "Pleasant place new",
            "action": "Pleasant action new",
            "is_pleasant": True,
            "time_needed": 90,
            "is_public": False,
            "time": "2025-03-30T17:30:00+03:00",
        }
        request = self.client.post(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.get("non_field_errors"),
            [
                "Pleasant habit is already reward, it can't have a related habit or reward "
                "and should not be performed regularly."
            ],
        )

    def test_habit_retrieve(self):
        url = reverse("habits:habit-detail", args=(self.good_habit.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("place"), "Place 1")
        self.assertEqual(response.get("user"), self.user.pk)

    def test_habit_retrieve_public_habit_error(self):
        url = reverse("habits:habit-detail", args=(self.pleasant_habit2.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.get("detail"), "You do not have permission to perform this action.")

    def test_habit_retrieve_non_public_habit_error(self):
        url = reverse("habits:habit-detail", args=(self.pleasant_habit3.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.get("detail"), "You do not have permission to perform this action.")

    def test_habit_list(self):
        url = reverse("habits:habit-list")
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "place": self.good_habit.place,
                        "time": self.good_habit.time,
                        "action": self.good_habit.action,
                        "is_pleasant": self.good_habit.is_pleasant,
                        "frequency": self.good_habit.frequency,
                        "reward": self.good_habit.reward,
                        "end_time": None,
                        "time_needed": self.good_habit.time_needed,
                        "is_public": self.good_habit.is_public,
                        "user": self.user.pk,
                        "related_habit": None,
                        "days_of_week": [],
                    },
                    {
                        "id": self.pleasant_habit.pk,
                        "place": self.pleasant_habit.place,
                        "time": self.pleasant_habit.time,
                        "action": self.pleasant_habit.action,
                        "is_pleasant": self.pleasant_habit.is_pleasant,
                        "frequency": "m h * * *",
                        "reward": None,
                        "end_time": None,
                        "time_needed": self.pleasant_habit.time_needed,
                        "is_public": self.pleasant_habit.is_public,
                        "user": self.user.pk,
                        "related_habit": None,
                        "days_of_week": [],
                    },
                ],
            },
        )

    def test_public_habit_list(self):
        url = reverse("habits:public-habit-list")
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            [
                {
                    "action": self.good_habit.action,
                    "is_pleasant": self.good_habit.is_pleasant,
                    "time_needed": self.good_habit.time_needed,
                },
                {
                    "action": self.pleasant_habit2.action,
                    "is_pleasant": self.pleasant_habit2.is_pleasant,
                    "time_needed": self.pleasant_habit2.time_needed,
                },
            ],
        )

    def test_habit_update(self):
        url = reverse("habits:habit-update", args=(self.good_habit.pk,))
        body = {
            "place": "Place new",
            "time": "2025-03-30T15:30:00+03:00",
            "action": "Action 1",
            "is_pleasant": False,
            "frequency": "m h * * *",
            "reward": "Reward 1",
            "time_needed": 90,
            "is_public": True,
        }
        request = self.client.patch(url, body, format="json")
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("place"), "Place new")

    def test_habit_delete(self):
        url = reverse("habits:habit-delete", args=(self.good_habit.pk,))
        request = self.client.delete(url)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 3)
