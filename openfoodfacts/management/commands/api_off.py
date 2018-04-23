import requests

from django.core.management.base import BaseCommand
from openfoodfacts.models import Categories, Products
from django.db import IntegrityError


class Command(BaseCommand):

    help = "Use it to update the database from OpenFoodFacts"

    def handle(self, *args, **kwargs):
        self.stdout.write("Updating PurBeurre's database.", ending='\n')

        categories = [
            "Biscuits et gâteaux",
            "Fromages",
            "Matières grasses",
            "Poduits à tartiner",
            "Petit-déjeuner",
            "Charcuteries",
            "Confiseries",
            "Boissons sucrées",
            "Jus et nectars de fruits",
            "Gateaux",
        ]

        for category in categories:
            products = self._request_api(category)
            self._insert(products)

    def _request_api(self, category):

        api_url = "https://fr.openfoodfacts.org/cgi/search.pl"

        params = {
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category,
            'action': 'process',
            'json': '1',
            'page_size': '1000'
        }

        try:
            products_data = requests.get(api_url, params=params)
            products_data = products_data.json()

            i = 0
            content = []
            for product in products_data["products"]:
                nutrichar = ['a','b','c','d','e']


                # Make sure that nutriscore have correct value
                if str(*products_data["products"][i]["nutrition_grades_tags"]) in nutrichar:
                    try:
                        cat = ''
                        cat = products_data["products"][i]["categories_prev_hierarchy"][:5]
                        extract_data= {
                            "product_name": products_data["products"][i]["product_name"],
                            "product_id": int(products_data["products"][i]["_id"]),
                            "product_url": products_data["products"][i]["url"],
                            "product_img": products_data["products"][i]["image_small_url"],
                            "nutriscore": str(*products_data["products"][i]["nutrition_grades_tags"]),
                            "fat": products_data["products"][i]["nutriments"]["fat_100g"],
                            "saturated_fat": products_data["products"][i]["nutriments"]["saturated-fat_100g"],
                            "salt": products_data["products"][i]["nutriments"]["salt_100g"],
                            "sugar": products_data["products"][i]["nutriments"]["sugars_100g"],
                            "categories": cat
                            }
                        content.append(extract_data)
                    except KeyError:
                        pass
                    except IndexError:
                        pass
                i += 1
            return content

        except requests.exceptions.ConnectionError:
            print("You must be connected in order to create/update database")

    def _insert(self, prod_data):
        for prod in prod_data:

            try:
                cat, created = Categories.objects.get_or_create(
                    category_name=prod["categories"]
                    )
                Products.objects.update_or_create(
                    id_product=prod["product_id"],
                    product_name=prod["product_name"],
                    url=prod["product_url"],
                    img=prod["product_img"],
                    nutriscore=prod["nutriscore"],
                    fat=prod["fat"],
                    saturated_fat=prod["saturated_fat"],
                    salt=prod["salt"],
                    sugar=prod["sugar"],
                    category=cat
                )
            # Ignore duplicate value
            except IntegrityError:
                continue
