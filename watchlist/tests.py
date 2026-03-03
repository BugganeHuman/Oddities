from rest_framework.test import APITestCase
from rest_framework import status
from .models import WatchlistItem


class WatchlistTest(APITestCase):

    def setUp(self):
        self.item = WatchlistItem.objects.create(name="Mr.Robot", year_start=2015, category="SR")
        self.url = f'/api/watchlist/item/{self.item.id}/'

    def test_create(self):
        el = {
        "name": "Ozark",
        "link": "",
        "year_start": 2017,
        "year_end": "",
        "category": "SR",
        "director": "",
        "synopsis": "",
        "runtime": "",
        "episodes": "",
        "seasons": "",
        }
        response = self.client.post("/api/watchlist/item/", el)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WatchlistItem.objects.filter(id=self.item.id))

    def test_update(self):
        new_data = {'name' : 'test'}
        response = self.client.patch(self.url, new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.item.refresh_from_db()

        self.assertEqual(self.item.name, 'test')