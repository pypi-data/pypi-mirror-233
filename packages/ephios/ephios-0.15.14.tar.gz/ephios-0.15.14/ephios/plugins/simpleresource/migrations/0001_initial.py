# Generated by Django 4.1.3 on 2022-12-24 15:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0014_auto_20211106_1852"),
    ]

    operations = [
        migrations.CreateModel(
            name="Resource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="ResourceCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="ResourceAllocation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("resources", models.ManyToManyField(blank=True, to="simpleresource.resource")),
                (
                    "shift",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.shift"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="resource",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="simpleresource.resourcecategory"
            ),
        ),
    ]
