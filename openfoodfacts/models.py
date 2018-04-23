from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    id_product = models.BigIntegerField(primary_key=True)
    product_name = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    img = models.URLField()
    fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    saturated_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    salt = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sugar = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    nutriscore = models.CharField(max_length=1, null=True)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)

    def __str__(self):
        return str({
            "id_product": self.id_product,
            "product_name": self.product_name,
            "url": self.url,
            "image": self.img,
            "nutriscore": self.nutriscore,
            "category": self.category
            })


class Substitutes(models.Model):
    origin = models.ForeignKey(Products, related_name="origin", on_delete=models.CASCADE)
    replacement = models.ForeignKey(Products, related_name="replacement", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str({
            "origin": self.origin,
            "replacement": self.replacement,
            "user": self.user
        })
