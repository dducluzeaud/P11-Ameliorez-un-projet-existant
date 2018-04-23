import json

from openfoodfacts.models import Categories, Products
from openfoodfacts.management.commands.api_off import Command
from django.test import TestCase



class CommandTestCase(TestCase):
    def setUp(self):
        self.com = Command()
        self.category = "Fromages"
        prod_data = {
            "product_name": "Comté",
            "product_id": 123,
            "product_url": "http://",
            "product_img": "http://",
            "nutriscore": "c",
            "fat": 6.3,
            "saturated_fat": 1,
            "salt": 0.1,
            "sugar": 13,
            "categories": ['en:plant-based-foods-and-beverages']
            }
        self.content = [prod_data]

    def test_handle(self):
        json_results = open("openfoodfacts/tests/mock_folder/off.json")
        mock = json.load(json_results)

        def mockreturn(a):
            return mock

        self.com._request_api = mockreturn
        self.com.handle()

        self.assertEqual(Products.objects.all().exists(), True)
        self.assertEqual(Categories.objects.all().exists(), True)
