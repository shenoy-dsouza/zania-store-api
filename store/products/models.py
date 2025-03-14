from django.db import models
import uuid
from django.core.validators import MinValueValidator


class Product(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(1)])  # Ensure price >= 0
    stock = models.IntegerField(validators=[MinValueValidator(1)])  # Ensure stock >= 0
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        db_table = "products"
        managed = True
