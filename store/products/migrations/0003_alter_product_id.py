# Generated by Django 5.1.7 on 2025-03-14 18:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_product_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.CharField(
                default=uuid.UUID("9573f9fb-ce7b-439f-b0f1-5e2566027cb8"),
                max_length=36,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
