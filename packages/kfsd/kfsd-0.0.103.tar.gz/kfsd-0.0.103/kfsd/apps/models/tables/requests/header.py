from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.requests.endpoint import Endpoint


class Header(BaseModel):
    endpoint = models.ForeignKey(
        Endpoint, on_delete=models.CASCADE, related_name="headers"
    )
    key = models.CharField(max_length=MAX_LENGTH)
    value = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.identifier = ",".join(
            [
                "{}".format(self.endpoint.identifier),
                "{}={}".format("HEADER", self.key),
            ]
        )
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Header"
        verbose_name_plural = "Headers"
