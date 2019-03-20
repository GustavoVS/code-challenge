import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Pdv
from ..serializers import PdvSerializer
from django.contrib.gis.geos import MultiPolygon, Polygon, Point


client = Client()


class CreatePdvTest(TestCase):

    def setUp(self):
        self.pdv_payload = {
            "tradingName": "Adega da Cerveja - Pinheiros",
            "ownerName": "Ze da Silva",
            "document": "1432132123891/0001",
            "coverageArea": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[30, 20], [45, 40], [10, 40], [30, 20]]],
                    [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
                ]
            },
            "address": {
                "type": "Point",
                "coordinates": [-46.57421, -21.785741]
            },
        }
        self.required_fields = (
            "tradingName",
            "ownerName",
            "document",
            "coverageArea",
            "address",
        )

    def post_payload(self, payload):
        return client.post(
            reverse('pdv-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )

    def test_create_valid_pdv(self):
        response = self.post_payload(self.pdv_payload)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Asserting can create a PDV"
        )

    def test_duplicate_document_pdv(self):
        response = self.post_payload(self.pdv_payload)
        response = self.post_payload(self.pdv_payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Asserting can't create a PDV with document duplicated"
        )

    def test_required_fields_pdv(self):

        for field in self.required_fields:
            invalid_payload = dict(self.pdv_payload)
            del invalid_payload[field]

            response = self.post_payload(invalid_payload)

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
                "Asserting can't create a PDV withtout a {}".format(field)
            )


class GetPdvTest(TestCase):

    def setUp(self):
        self.pdv1 = Pdv.objects.create(
            trading_name="Adega 1",
            owner_name="Ze Um",
            document="1432132123891/0001",
            coverage_area=MultiPolygon(
                Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
                Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
            ),
            address=Point(1, 1)
        )

        self.pdv2 = Pdv.objects.create(
            trading_name="Adega 2",
            owner_name="Ze Dois",
            document="1432132123891/0002",
            coverage_area=MultiPolygon(
                Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
                Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
            ),
            address=Point(0, 1)
        )

        self.pdv3 = Pdv.objects.create(
            trading_name="Adega 3",
            owner_name="Ze Tres",
            document="1432132123891/0003",
            coverage_area=MultiPolygon(
                Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
                Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
            ),
            address=Point(1, 0)
        )

    def test_get_valid_pdv(self):
        response = client.get(reverse('pdv-detail', kwargs={'pk': self.pdv2.pk}))
        serializer = PdvSerializer(self.pdv2)

        self.assertEqual(
            response.data,
            serializer.data,
            "Asserting data when get a pdv"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Asserting status when get a pdv"
        )

    def test_get_invalid_pdv(self):
        response = client.get(reverse('pdv-detail', kwargs={'pk': 300}))
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Asserting status when get a invalid pdv"
        )


class SearchPdvTest(TestCase):

    def setUp(self):
        self.pdv1 = Pdv.objects.create(
            trading_name="Adega 1",
            owner_name="Ze Um",
            document="1432132123891/0001",
            coverage_area=MultiPolygon(Polygon(
                ((0, 0), (0, 6), (6, 6), (6, 3), (0, 0))
            )),
            address=Point(1, 2)
        )
        self.pdv2 = Pdv.objects.create(
            trading_name="Adega 2",
            owner_name="Ze Dois",
            document="1432132123891/0002",
            coverage_area=MultiPolygon(Polygon(
                ((2, 5), (2, 10), (6, 10), (5, 6), (2, 5))
            )),
            address=Point(3, 9)
        )
        self.pdv3 = Pdv.objects.create(
            trading_name="Adega 3",
            owner_name="Ze Tres",
            document="1432132123891/0003",
            coverage_area=MultiPolygon(Polygon(
                ((2, 5), (3, 7), (9, 7), (6, 5), (2, 5))
            )),
            address=Point(7, 6)
        )

    def search_pdv(self, lng, lat):
        return client.get("{}?lng={}&lat={}".format(reverse('search-pdv'), lng, lat))

    def test_search_inside_one(self):
        # point (4, 9) inside coverage area of pdv2 only
        response = self.search_pdv(4, 9)
        serializer = PdvSerializer(self.pdv2)

        self.assertEqual(
            response.data,
            serializer.data,
            "Asserting is the correct pdv"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Asserting status of request"
        )

    def test_search_inside_three(self):
        # point (5, 6) inside coverage area of the three, closer is pdv3
        response = self.search_pdv(5, 6)
        serializer = PdvSerializer(self.pdv3)

        self.assertEqual(
            response.data,
            serializer.data,
            "Asserting is the correct pdv"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Asserting status of request"
        )

    def test_search_outside(self):
        # point (10, 10) is outside of PDVs
        response = self.search_pdv(10, 10)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "Asserting status when PDV is not found"
        )
