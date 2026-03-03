from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Title


class TitleTest(TestCase):

    def test_create(self):
        title = Title.objects.create(name="Ozark", year_start=2017, director="J",
            category="SR", cover="https://media.themoviedb.org/t/p/"
            "w300_and_h450_face/pCGyPVrI9Fzw6rE1Pvi4BIXF6ET.jpg",
            start_watch="2026-03-03", end_watch="2026-03-04", status="DONE",
            review="ok 6.5", rating=6.5)
        self.assertEqual(title.name, "Ozark")
        self.assertEqual(title.rating, 6.5)
        self.assertEqual(Title.objects.count(), 1)




class TitleApiTests(APITestCase):

    def setUp(self):
        self.title = Title.objects.create(name="Ozark", year_start=2017, director="J",
            category="SR", cover="https://media.themoviedb.org/t/p/"
            "w300_and_h450_face/pCGyPVrI9Fzw6rE1Pvi4BIXF6ET.jpg",
            start_watch="2026-03-03", end_watch="2026-03-04", status="DONE",
            review="ok 6.5", rating=6.5)
        self.url = f'/api/titles/title/{self.title.id}/'

    def test_create(self):
        el = {
            "name": "Ozark",
            "year_start": 2017,
            "year_end": 2022,
            "director": "Jason Bateman",
            "category": "SR",
            "cover": "https://www.themoviedb.org/t/p/w600_and_h900_face/pCGyPVrI9Fzw6rE1Pvi4BIXF6ET.jpg",
            "start_watch": "2026-03-01",
            "end_watch": "2026-03-03",
            "status": "DONE",
            "review": "ok 6.5",
            "rating": "6.5",
        }

        act = self.client.post("/api/titles/title/", el)

        self.assertEqual(act.status_code, 201)
        #self.assertEqual(Title.objects.count(), 2)


    def test_delete(self):
        el = Title.objects.create(name="Ozark", year_start=2017, director="J",
            category="SR", cover="https://media.themoviedb.org/t/p/"
            "w300_and_h450_face/pCGyPVrI9Fzw6rE1Pvi4BIXF6ET.jpg",
            start_watch="2026-03-03", end_watch="2026-03-04", status="DONE",
            review="ok 6.5", rating=6.5)


        response = self.client.delete(f"/api/titles/title/{el.id}/")

        self.assertEqual(response.status_code, 204)
        #self.assertEqual(Title.objects.count(), 0)
        self.assertFalse(Title.objects.filter(id=el.id).exists())

    def test_update(self):
        new_data = {'director' : 'q'}
        response = self.client.patch(self.url, new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.title.refresh_from_db()

        self.assertEqual(self.title.director, 'q')