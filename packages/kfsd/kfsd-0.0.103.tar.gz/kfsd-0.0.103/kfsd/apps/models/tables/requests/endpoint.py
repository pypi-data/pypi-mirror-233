from django.db import models

from kfsd.apps.models.constants import MAX_LENGTH
from kfsd.apps.models.tables.base import BaseModel
from kfsd.apps.models.tables.general.data import Data


class Endpoint(BaseModel):
    METHOD_CHOICES = (
        ("POST", "POST"),
        ("GET", "GET"),
        ("DELETE", "DELETE"),
    )
    name = models.CharField(max_length=MAX_LENGTH)
    url = models.TextField()
    method = models.CharField(
        choices=METHOD_CHOICES, default="GET", max_length=MAX_LENGTH
    )
    body = models.ForeignKey(
        Data,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="data",
    )
    success_code = models.IntegerField()

    def save(self, *args, **kwargs):
        self.identifier = ",".join(
            [
                "{}={}".format("ENDPOINT", self.name),
                "{}={}".format("METHOD", self.method),
            ]
        )
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"
