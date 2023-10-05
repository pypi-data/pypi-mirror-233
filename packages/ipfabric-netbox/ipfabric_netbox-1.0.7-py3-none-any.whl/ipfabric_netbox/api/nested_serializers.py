from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer

from ipfabric_netbox.models import IPFabricSnapshot
from ipfabric_netbox.models import IPFabricSource
from ipfabric_netbox.models import IPFabricTransformMap

__all__ = (
    "NestedIPFabricSourceSerializer",
    "NestedIPFabricSnapshotSerializer",
    "NestedIPFabricTransformMapSerializer",
)


class NestedIPFabricSourceSerializer(NetBoxModelSerializer):
    class Meta:
        model = IPFabricSource
        fields = ["id", "url", "display", "name"]


class NestedIPFabricSnapshotSerializer(NetBoxModelSerializer):
    source = NestedIPFabricSourceSerializer(read_only=True)

    class Meta:
        model = IPFabricSnapshot
        fields = ["id", "name", "source", "snapshot_id", "date", "display", "sites"]


class NestedIPFabricTransformMapSerializer(NetBoxModelSerializer):
    target_model = ContentTypeField(read_only=True)

    class Meta:
        model = IPFabricTransformMap
        fields = [
            "id",
            "source_model",
            "target_model",
            "status",
        ]
