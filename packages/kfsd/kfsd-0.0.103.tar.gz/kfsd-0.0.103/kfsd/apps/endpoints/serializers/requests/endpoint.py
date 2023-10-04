from rest_framework import serializers

from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from kfsd.apps.models.constants import MAX_LENGTH, MIN_LENGTH

from kfsd.apps.endpoints.serializers.model import BaseModelSerializer
from kfsd.apps.endpoints.serializers.requests.header import HeaderViewModelSerializer
from kfsd.apps.models.tables.requests.endpoint import Endpoint
from kfsd.apps.models.tables.general.data import Data


class EndpointModelSerializer(BaseModelSerializer):
    name = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(MIN_LENGTH),
            MaxLengthValidator(MAX_LENGTH),
        ],
    )

    url = serializers.CharField(
        required=True,
        validators=[
            MinLengthValidator(MIN_LENGTH),
        ],
    )

    method = serializers.ChoiceField(choices=["GET", "POST", "PATCH", "PUT", "DELETE"])

    body = serializers.SlugRelatedField(
        required=True,
        many=False,
        read_only=False,
        slug_field="identifier",
        queryset=Data.objects.all(),
    )

    headers = HeaderViewModelSerializer(many=True, read_only=True)

    success_code = serializers.IntegerField(default=200)

    class Meta:
        model = Endpoint
        fields = "__all__"


class EndpointViewModelSerializer(EndpointModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = Endpoint
        exclude = ("created", "updated", "id")
