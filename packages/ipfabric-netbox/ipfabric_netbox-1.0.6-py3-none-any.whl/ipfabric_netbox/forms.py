import copy

from core.choices import DataSourceStatusChoices
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext as _
from extras.choices import DurationChoices
from extras.forms.mixins import SavedFiltersMixin
from netbox.forms import NetBoxModelFilterSetForm
from netbox.forms import NetBoxModelForm
from utilities.forms import add_blank_choice
from utilities.forms import BootstrapMixin
from utilities.forms import FilterForm
from utilities.forms import get_field_value
from utilities.forms.fields import CommentField
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.fields import DynamicModelMultipleChoiceField
from utilities.forms.widgets import APISelectMultiple
from utilities.forms.widgets import DateTimePicker
from utilities.forms.widgets import HTMXSelect
from utilities.forms.widgets import NumberWithOptions
from utilities.utils import local_now

from .choices import transform_field_source_columns
from .models import IPFabricBranch
from .models import IPFabricRelationshipField
from .models import IPFabricSnapshot
from .models import IPFabricSource
from .models import IPFabricSync
from .models import IPFabricTransformField
from .models import IPFabricTransformMap

exclude_fields = [
    "id",
    "created",
    "last_updated",
    "custom_field_data",
    "_name",
    "status",
]


class IPFSiteChoiceField(forms.MultipleChoiceField):
    def valid_value(self, value):
        """Check to see if the provided value is a valid choice."""
        text_value = str(value)
        for k, v in self.choices:
            if isinstance(v, (list, tuple)):
                for k2, v2 in v:
                    if value == k2 or text_value == str(k2):
                        return True
            else:
                if value == k or text_value == str(k):
                    return True
        return False


dcim_parameters = {
    "site": forms.BooleanField(required=False, label=_("Sites"), initial=True),
    "manufacturer": forms.BooleanField(
        required=False, label=_("Manufacturers"), initial=True
    ),
    "devicetype": forms.BooleanField(
        required=False, label=_("Device Types"), initial=True
    ),
    "devicerole": forms.BooleanField(
        required=False, label=_("Device Roles"), initial=True
    ),
    "platform": forms.BooleanField(required=False, label=_("Platforms"), initial=True),
    "device": forms.BooleanField(required=False, label=_("Devices"), initial=True),
    "virtualchassis": forms.BooleanField(
        required=False, label=_("Virtual Chassis"), initial=True
    ),
    "interface": forms.BooleanField(required=False, label=_("Interfaces")),
    # TODO: Inventory Item broken util https://github.com/netbox-community/netbox/issues/13422 is resolved
    # "inventoryitem": forms.BooleanField(required=False, label=_("Part Numbers")),
}
ipam_parameters = {
    "vlan": forms.BooleanField(required=False, label=_("VLANs")),
    "vrf": forms.BooleanField(required=False, label=_("VRFs")),
    "prefix": forms.BooleanField(required=False, label=_("Prefixes")),
    "ipaddress": forms.BooleanField(required=False, label=_("IP Addresses")),
}
sync_parameters = {"dcim": dcim_parameters, "ipam": ipam_parameters}


def source_column_choices(model):
    columns = transform_field_source_columns.get(model, None)
    if columns:
        choices = [(f, f) for f in transform_field_source_columns.get(model)]
    else:
        choices = []
    return choices


def add_all_sites(choices):
    """
    Add a blank choice to the beginning of a choices list.
    """
    return ((None, "All Sites"),) + tuple(choices)


def str_to_list(str):
    if not isinstance(str, list):
        return [str]
    else:
        return str


def list_to_choices(choices):
    new_choices = ()
    for choice in choices:
        new_choices = new_choices + ((choice, choice),)
    return new_choices


class IPFabricRelationshipFieldForm(BootstrapMixin, forms.ModelForm):
    coalesce = forms.BooleanField(required=False, initial=False)
    target_field = forms.CharField(
        label="Target Field",
        required=True,
        help_text="Select target model field.",
        widget=forms.Select(),
    )

    fieldsets = (
        (
            "Transform Map",
            ("transform_map", "source_model", "target_field", "coalesce"),
        ),
        ("Extras", ("template",)),
    )

    class Meta:
        model = IPFabricRelationshipField
        fields = (
            "transform_map",
            "source_model",
            "target_field",
            "coalesce",
            "template",
        )
        widgets = {
            "transform_map": HTMXSelect(),
        }
        help_texts = {
            "link_text": _(
                "Jinja2 template code for the source field. Reference the object as <code>{{ object }}</code>. "
                "templates which render as empty text will not be displayed."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data:
            if self.instance and self.instance.pk is not None:
                fields = (
                    self.instance.transform_map.target_model.model_class()._meta.fields
                )
                self.fields["target_field"].widget.choices = add_blank_choice(
                    [
                        (f.name, f.verbose_name)
                        for f in fields
                        if f.is_relation and f.name not in exclude_fields
                    ]
                )
                self.fields["target_field"].widget.initial = self.instance.target_field
            else:
                if kwargs["initial"].get("transform_map", None):
                    transform_map_id = kwargs["initial"]["transform_map"]
                    transform_map = IPFabricTransformMap.objects.get(
                        pk=transform_map_id
                    )
                    fields = transform_map.target_model.model_class()._meta.fields
                    choices = [
                        (f.name, f.verbose_name)
                        for f in fields
                        if f.is_relation and f.name not in exclude_fields
                    ]
                    self.fields["target_field"].widget.choices = add_blank_choice(
                        choices
                    )


class IPFabricTransformFieldForm(BootstrapMixin, forms.ModelForm):
    coalesce = forms.BooleanField(required=False, initial=False)
    source_field = forms.CharField(
        label="Source Field",
        required=True,
        help_text="Select column from IP Fabric.",
        widget=forms.Select(),
    )
    target_field = forms.CharField(
        label="Target Field",
        required=True,
        help_text="Select target model field.",
        widget=forms.Select(),
    )

    fieldsets = (
        (
            "Transform Map",
            ("transform_map", "source_field", "target_field", "coalesce"),
        ),
        ("Extras", ("template",)),
    )

    class Meta:
        model = IPFabricTransformField
        fields = (
            "transform_map",
            "source_field",
            "target_field",
            "coalesce",
            "template",
        )
        widgets = {
            "template": forms.Textarea(attrs={"class": "font-monospace"}),
            "transform_map": HTMXSelect(),
        }
        help_texts = {
            "link_text": _(
                "Jinja2 template code for the source field. Reference the object as <code>{{ object }}</code>. "
                "templates which render as empty text will not be displayed."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data:
            if self.instance and self.instance.pk is not None:
                fields = (
                    self.instance.transform_map.target_model.model_class()._meta.fields
                )
                source_fields = self.instance.transform_map.source_model
                self.fields["target_field"].widget.choices = add_blank_choice(
                    [
                        (f.name, f.verbose_name)
                        for f in fields
                        if not f.is_relation and f.name not in exclude_fields
                    ]
                )
                self.fields["target_field"].widget.initial = self.instance.target_field
                self.fields["source_field"].widget.choices = add_blank_choice(
                    source_column_choices(source_fields)
                )
            else:
                if kwargs["initial"].get("transform_map", None):
                    transform_map_id = kwargs["initial"]["transform_map"]
                    transform_map = IPFabricTransformMap.objects.get(
                        pk=transform_map_id
                    )
                    fields = transform_map.target_model.model_class()._meta.fields
                    choices = [
                        (f.name, f.verbose_name)
                        for f in fields
                        if not f.is_relation and f.name not in exclude_fields
                    ]
                    self.fields["target_field"].widget.choices = add_blank_choice(
                        choices
                    )
                    self.fields["source_field"].widget.choices = add_blank_choice(
                        source_column_choices(transform_map.source_model)
                    )


class IPFabricTransformMapForm(BootstrapMixin, forms.ModelForm):
    status = forms.CharField(
        required=False,
        label=_("Status"),
        widget=forms.Select(),
    )

    class Meta:
        model = IPFabricTransformMap
        fields = ("name", "source_model", "target_model", "status")
        widgets = {
            "target_model": HTMXSelect(hx_url="/plugins/ipfabric/transform-map/add"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data:
            if kwargs["initial"].get("target_model"):
                target_model = ContentType.objects.get(
                    pk=kwargs["initial"].get("target_model")
                )
                try:
                    status = target_model.model_class()._meta.get_field("status")
                    self.fields["status"].widget.choices = add_blank_choice(
                        status.choices
                    )
                    self.fields["status"].widget.initial = get_field_value(
                        self, "status"
                    )
                except Exception as e:  # noqa: F841
                    self.fields["status"].widget.attrs["disabled"] = "disabled"
            else:
                if self.instance and self.instance.pk is not None:
                    transform_map = self.instance.target_model.model_class()
                    try:
                        status = transform_map._meta.get_field("status")
                        self.fields["status"].widget.choices = add_blank_choice(
                            status.choices
                        )
                        self.fields["status"].widget.initial = get_field_value(
                            self, "status"
                        )
                    except Exception as e:  # noqa: F841
                        self.fields["status"].widget.attrs["disabled"] = "disabled"


class IPFabricSnapshotFilterForm(NetBoxModelFilterSetForm):
    model = IPFabricSnapshot
    fieldsets = (
        (None, ("q", "filter_id")),
        ("Source", ("source_id",)),
    )
    source_id = DynamicModelMultipleChoiceField(
        queryset=IPFabricSource.objects.all(), required=False, label=_("Source")
    )


class IPFabricSourceFilterForm(NetBoxModelFilterSetForm):
    model = IPFabricSource
    fieldsets = (
        (None, ("q", "filter_id")),
        ("Data Source", ("status",)),
    )
    status = forms.MultipleChoiceField(choices=DataSourceStatusChoices, required=False)


class IPFabricBranchFilterForm(SavedFiltersMixin, FilterForm):
    fieldsets = (
        (None, ("q", "filter_id")),
        ("Source", ("sync_id",)),
    )
    model = IPFabricBranch
    sync_id = DynamicModelMultipleChoiceField(
        queryset=IPFabricSync.objects.all(), required=False, label=_("Sync")
    )


class IPFabricSourceForm(NetBoxModelForm):
    comments = CommentField()
    auth = forms.CharField(
        required=True,
        label=_("API Token"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text=_("IP Fabric API Token."),
    )
    verify = forms.BooleanField(
        required=False,
        initial=True,
        help_text=_(
            "Certificate validation. Uncheck if using self signed certificate."
        ),
    )

    class Meta:
        model = IPFabricSource
        fields = [
            "name",
            "url",
            "auth",
            "verify",
            "description",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            for name, form_field in self.instance.parameters.items():
                self.fields[name].initial = self.instance.parameters.get(name)

    def save(self, *args, **kwargs):
        parameters = {}
        for name in self.fields:
            if name.startswith("auth"):
                parameters["auth"] = self.cleaned_data[name]
            if name.startswith("verify"):
                parameters["verify"] = self.cleaned_data[name]

        self.instance.parameters = parameters
        self.instance.status = DataSourceStatusChoices.NEW

        return super().save(*args, **kwargs)


class IPFabricSyncForm(NetBoxModelForm):
    source = DynamicModelChoiceField(
        queryset=IPFabricSource.objects.all(),
        required=True,
        label=_("IP Fabric Source"),
    )
    snapshot_data = DynamicModelChoiceField(
        queryset=IPFabricSnapshot.objects.all(),
        required=True,
        label=_("Snapshot"),
        query_params={
            "source_id": "$source",
        },
    )

    sites = forms.MultipleChoiceField(
        required=False,
        label=_("Sites"),
        widget=APISelectMultiple(
            api_url="/api/plugins/ipfabric/snapshot/{{snapshot_data}}/sites/",
        ),
    )

    scheduled = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(),
        label=_("Schedule at"),
        help_text=_("Schedule execution of sync to a set time"),
    )
    interval = forms.IntegerField(
        required=False,
        min_value=1,
        label=_("Recurs every"),
        widget=NumberWithOptions(options=DurationChoices),
        help_text=_("Interval at which this sync is re-run (in minutes)"),
    )

    class Meta:
        model = IPFabricSync
        fields = (
            "name",
            "source",
            "snapshot_data",
            "sites",
            "type",
            "tags",
            "scheduled",
            "interval",
        )
        widgets = {
            "type": HTMXSelect(),
        }

    @property
    def fieldsets(self):
        fieldsets = [
            (
                "IP Fabric Source",
                ("name", "source", "snapshot_data", "sites", "type"),
            ),
        ]
        if self.backend_fields:
            for k, v in self.backend_fields.items():
                fieldsets.append((f"{k.upper()} Sync Parameters", v))
        fieldsets.append(("Ingestion Execution Parameters", ("scheduled", "interval")))
        fieldsets.append(("Tags", ("tags",)))

        return fieldsets

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.data:
            if sites := get_field_value(self, "sites"):
                sites = list_to_choices(str_to_list(sites))
                self.fields["sites"].choices = sites
                self.fields["sites"].initial = sites
        else:
            if snapshot_id := self.data.get("snapshot_data"):
                snapshot_sites = IPFabricSnapshot.objects.get(pk=snapshot_id).sites
                choices = list_to_choices(str_to_list(snapshot_sites))
                self.fields["sites"].choices = choices

        if self.instance and self.instance.pk:
            if not self.data:
                self.fields["sites"].choices = list_to_choices(
                    self.instance.snapshot_data.sites
                )
            self.initial["source"] = self.instance.snapshot_data.source
            self.initial["sites"] = self.instance.parameters["sites"]

        backend_type = get_field_value(self, "type")
        backend = {}
        if backend_type == "all":
            backend = sync_parameters
        else:
            backend[backend_type] = sync_parameters.get(backend_type)

        now = local_now().strftime("%Y-%m-%d %H:%M:%S")
        self.fields["scheduled"].help_text += f" (current time: <strong>{now}</strong>)"

        # Add backend-specific form fields
        self.backend_fields = {}
        for k, v in backend.items():
            self.backend_fields[k] = []
            for name, form_field in v.items():
                field_name = f"ipf_{name}"
                self.backend_fields[k].append(field_name)
                self.fields[field_name] = copy.copy(form_field)
                if self.instance and self.instance.parameters:
                    self.fields[field_name].initial = self.instance.parameters.get(name)

    def clean(self):
        super().clean()
        snapshot = self.cleaned_data["snapshot_data"]

        sites = self.data.get("sites")
        choices = list_to_choices(str_to_list(sites))
        self.fields["sites"].choices = choices

        if sites:
            if not any(y in x for x in snapshot.sites for y in sites):
                raise ValidationError({"sites": f"{sites} not part of the snapshot."})

        scheduled_time = self.cleaned_data.get("scheduled")
        if scheduled_time and scheduled_time < local_now():
            raise forms.ValidationError(_("Scheduled time must be in the future."))

        # When interval is used without schedule at, schedule for the current time
        if self.cleaned_data.get("interval") and not scheduled_time:
            self.cleaned_data["scheduled"] = local_now()

        return self.cleaned_data

    def save(self, *args, **kwargs):
        parameters = {}
        for name in self.fields:
            if name.startswith("ipf_"):
                parameters[name[4:]] = self.cleaned_data[name]
            if name == "sites":
                parameters["sites"] = self.cleaned_data["sites"]
        self.instance.parameters = parameters

        object = super().save(*args, **kwargs)
        if object.scheduled:
            object.enqueue_sync_job()
        return object


class SyncForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.snapshots = kwargs.pop("snapshot_choices", None)
        self.sites = kwargs.pop("site_choices", None)
        super(SyncForm, self).__init__(*args, **kwargs)
        if self.snapshots:
            snapshot_choices = [
                (snapshot_id, snapshot_name)
                for snapshot_name, snapshot_id in self.snapshots.values()
            ]
            self.fields["snapshot"] = forms.ChoiceField(
                label="Snapshot",
                required=True,
                choices=snapshot_choices,
                help_text="IPFabric snapshot to sync from. Defaults to $last",
                widget=forms.Select(
                    attrs={
                        "hx-get": reverse("plugins:ipfabric_netbox:ipfabricsync_add"),
                        "hx-trigger": "change",
                        "hx-target": "#modules",
                        "class": "form-control",
                    }
                ),
            )
        if self.sites:
            site_choices = [(site, site) for site in self.sites]
            self.fields["site"] = forms.ChoiceField(
                label="Site",
                required=False,
                choices=add_blank_choice(site_choices),
                help_text="Sites available within snapshot",
                widget=forms.Select(attrs={"class": "form-control"}),
            )
        else:
            self.fields["site"] = forms.ChoiceField(
                label="Site",
                required=False,
                choices=add_blank_choice([]),
                help_text="Sites available within snapshot",
                widget=forms.Select(
                    attrs={"class": "form-control", "disabled": "disabled"}
                ),
            )
