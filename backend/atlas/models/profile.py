from uuid import uuid4

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    dob = models.DateField(null=True)
    date_started = models.DateField(null=True)
    title = models.TextField(null=True)
    reports_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="reports",
    )
    office = models.ForeignKey("atlas.Office", null=True, on_delete=models.SET_NULL)
    photo_url = models.URLField(null=True)
    department = models.TextField(null=True)
    config = JSONField(default=dict)

    class Meta:
        db_table = "profile"
