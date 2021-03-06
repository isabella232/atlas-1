from uuid import uuid4

from django.db import models


class OfficeManager(models.Manager):
    def get_by_natural_key(self, external_id):
        return self.get(external_id=external_id)

    def get_or_create_by_natural_key(self, external_id):
        return self.get_or_create(
            external_id=external_id, defaults={"name": external_id}
        )


class Office(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    external_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    location = models.TextField(null=True)
    region_code = models.CharField(max_length=64, null=True)
    postal_code = models.CharField(max_length=64, null=True)
    administrative_area = models.CharField(max_length=64, null=True)
    locality = models.CharField(max_length=64, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    objects = OfficeManager()

    class Meta:
        db_table = "office"

    def natural_key(self):
        return [self.external_id]
