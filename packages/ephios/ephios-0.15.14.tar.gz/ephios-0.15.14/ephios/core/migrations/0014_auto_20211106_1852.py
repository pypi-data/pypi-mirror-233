# Generated by Django 3.2.9 on 2021-11-06 17:52

import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_auto_20211027_2203"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="event",
            options={
                "base_manager_name": "all_objects",
                "default_manager_name": "objects",
                "permissions": [("view_past_event", "Can view past events")],
                "verbose_name": "event",
                "verbose_name_plural": "events",
            },
        ),
        migrations.AlterModelManagers(
            name="event",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("all_objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name="eventtype",
            name="can_grant_qualification",
        ),
        migrations.AddField(
            model_name="abstractparticipation",
            name="comment",
            field=models.CharField(blank=True, max_length=255, verbose_name="Comment"),
        ),
        migrations.AddField(
            model_name="abstractparticipation",
            name="individual_end_time",
            field=models.DateTimeField(null=True, verbose_name="individual end time"),
        ),
        migrations.AddField(
            model_name="abstractparticipation",
            name="individual_start_time",
            field=models.DateTimeField(null=True, verbose_name="individual start time"),
        ),
        migrations.AddField(
            model_name="notification",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="abstractparticipation",
            name="state",
            field=models.IntegerField(
                choices=[
                    (0, "requested"),
                    (1, "confirmed"),
                    (2, "declined by user"),
                    (3, "rejected by responsible"),
                    (4, "getting dispatched"),
                ],
                default=4,
                verbose_name="state",
            ),
        ),
        migrations.AlterField(
            model_name="localparticipation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="participations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Participant",
            ),
        ),
    ]
