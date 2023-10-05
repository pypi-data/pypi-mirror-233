from django.db import connection
from extras.plugins import PluginConfig


class NetboxIPFabricConfig(PluginConfig):
    name = "ipfabric_netbox"
    verbose_name = "NetBox IP Fabric SoT Plugin"
    description = "Sync IP Fabric into NetBox"
    version = "1.0.7"
    base_url = "ipfabric"

    def ready(self):
        super().ready()
        from ipfabric_netbox.signals import ipfabric_netbox_init

        all_tables = connection.introspection.table_names()
        if "extras_customfield" in all_tables:
            ipfabric_netbox_init()


config = NetboxIPFabricConfig
