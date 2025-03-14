from django.conf import settings
from django.db import migrations

def seed_products(apps, schema_editor):
    # Prevent seeding when running tests
    if getattr(settings, "TEST", False):
        return

    Product = apps.get_model('products', 'Product')  # Get the Product model
    products_data = [
        {"name": "Laptop", "price": 999.99, "stock": 10},
        {"name": "Smartphone", "price": 499.99, "stock": 20},
        {"name": "Headphones", "price": 99.99, "stock": 50},
    ]
    for product in products_data:
        Product.objects.create(**product)

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_products),
    ]
