from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.general.data import Data
from kfsd.apps.endpoints.serializers.general.data import DataViewModelSerializer
from kfsd.apps.endpoints.views.general.docs.data import DataDoc


@extend_schema_view(**DataDoc.modelviewset())
class DataModelViewSet(CustomModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataViewModelSerializer
