from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Teaser


User = get_user_model()


class AccountTests(APITestCase):
    # Enforce proper typehinting
    client: APIClient

    def setUp(self):
        self.admin = User.objects.create(username="admin", is_staff=True)
        self.admin.set_password("verystrongpassword")
        self.admin.save()

        self.user = User.objects.create(username="user", is_staff=False)
        self.user.set_password("verystrongpassword")
        self.user.save()

    def _create_teaser(self, user: User, data: dict):
        """Creates a teaser with passed data and user instance.

        @user: user instance
        @data: request payload
        """
        self.client.force_authenticate(user=user)
        return self.client.post(reverse("teaser-list"), data=data)

    def _list_teasers(self, user: User, my: bool = False):
        """Get created teasers list

        @user: user instance
        @my: use `/my` endpoint instead"""
        self.client.force_authenticate(user)
        return self.client.get(reverse("teaser-my" if my else "teaser-list"))

    def test_create_admin_teaser(self):
        data = {
            "title": "Admin's First Teaser",
            "description": "Admin's First Teaser Description Text",
        }

        response = self._create_teaser(self.admin, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], data["title"])
        self.assertEqual(response.json()["description"], data["description"])

    def test_create_user_teaser(self):
        data = {
            "title": "User's First Teaser",
            "description": "User's First Teaser Description Text",
        }

        response = self._create_teaser(self.user, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], data["title"])
        self.assertEqual(response.json()["description"], data["description"])

    def test_list_teasers_admin_no_teasers(self):
        response = self._list_teasers(self.admin)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_list_teasers_user_redirect(self):
        response = self._list_teasers(self.user)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_my_teasers_user_no_teasers(self):
        response = self._list_teasers(self.user, True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_my_teasers_admin_no_teasers(self):
        response = self._list_teasers(self.admin, True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_list_teasers_admin_has_teasers(self):
        self.test_create_admin_teaser()
        self.test_create_user_teaser()

        response = self._list_teasers(self.admin)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_my_teasers_admin_has_teasers(self):
        self.test_create_admin_teaser()

        response = self._list_teasers(self.admin)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_list_teasers_user_has_teasers(self):
        self.test_create_user_teaser()
        self.test_create_admin_teaser()

        response = self._list_teasers(self.user)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        response = self._list_teasers(self.user, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_user_change_teaser_status_unchanged(self):
        self.test_create_user_teaser()
        teaser = Teaser.objects.filter(author=self.user).first()

        url = "%s%s/" % (reverse("teaser-list"), str(teaser.id))
        data = {
            "title": "Abracadabra",
            "status": Teaser.Status.PAID,
        }

        self.client.force_authenticate(user=self.user)
        self.client.patch(url, data=data)

        teaser.refresh_from_db()

        self.assertEqual(teaser.title, data["title"])
        self.assertEqual(teaser.status, Teaser.Status.PENDING)

    def test_admin_change_teaser_status_changed(self):
        self.test_create_user_teaser()
        teaser = Teaser.objects.filter(author=self.user).first()

        url = "%s%s/" % (reverse("teaser-list"), str(teaser.id))
        data = {
            "title": "Abracadabra",
            "status": Teaser.Status.PAID,
        }

        self.client.force_authenticate(user=self.admin)
        self.client.patch(url, data=data)

        teaser.refresh_from_db()

        self.assertEqual(teaser.title, data["title"])
        self.assertEqual(teaser.status, Teaser.Status.PAID)

    def test_admin_change_teaser_status_changed_locked(self):
        self.test_create_user_teaser()
        teaser = Teaser.objects.filter(author=self.user).first()

        url = "%s%s/" % (reverse("teaser-list"), str(teaser.id))

        self.client.force_authenticate(user=self.admin)
        self.client.patch(url, data={"status": Teaser.Status.PAID})

        teaser.refresh_from_db()
        self.assertEqual(teaser.status, Teaser.Status.PAID)

        response = self.client.patch(url, data={"status": Teaser.Status.PENDING})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        teaser.refresh_from_db()
        self.assertEqual(teaser.status, Teaser.Status.PAID)
