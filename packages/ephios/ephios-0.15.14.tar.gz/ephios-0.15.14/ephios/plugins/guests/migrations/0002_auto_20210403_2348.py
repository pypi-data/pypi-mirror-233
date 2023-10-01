# Generated by Django 3.1.7 on 2021-04-03 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("guests", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guestparticipation",
            name="guest_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="guests.guestuser",
                verbose_name="guest participant",
            ),
        ),
    ]
