# Generated by Django 5.1.7 on 2025-03-14 18:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="id",
            field=models.CharField(
                default=uuid.UUID("0ac91bc8-6cb1-4d6e-8122-6214a060358b"),
                max_length=36,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
