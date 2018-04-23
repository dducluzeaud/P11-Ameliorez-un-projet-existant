from django.test import TestCase
from openfoodfacts.models import Categories, Products


class CategoriesTestCase(TestCase):
    def setUp(self):
        c = Categories.objects.create(category_name="confitures")

    def test_category_name(self):
        marmelade = Categories.objects.get(category_name="confitures")
        self.assertEqual("confitures", marmelade.category_name)


class ProductsTestCase(TestCase):
    def setUp(self):
        cat, created = Categories.objects.get_or_create(
            category_name="Pâtes à tartiner"
            )

        Products.objects.create(
            id_product=1,
            product_name="nutella",
            url="http://",
            img="http://",
            nutriscore="e",
            category= cat)

    def test_id_product(self):
        nutella = Products.objects.get(id_product=1)
        self.assertEqual(1, nutella.id_product)

    def test_product_name(self):
        nutella = Products.objects.get(product_name="nutella")
        self.assertEqual("nutella", nutella.product_name)

    def test_url(self):
        nutella = Products.objects.get(url="http://")
        self.assertEqual("http://", nutella.url)

    def test_img(self):
        nutella = Products.objects.get(img="http://")
        self.assertEqual("http://", nutella.img)

    def test_nutriscore(self):
        nutella = Products.objects.get(nutriscore="e")
        self.assertEqual("e", nutella.nutriscore)

    def test_category_id(self):
        nutella = Products.objects.get(product_name="nutella")
        cat = Categories.objects.get(category_name="Pâtes à tartiner")
        self.assertEqual(str(nutella.category), cat.category_name)
