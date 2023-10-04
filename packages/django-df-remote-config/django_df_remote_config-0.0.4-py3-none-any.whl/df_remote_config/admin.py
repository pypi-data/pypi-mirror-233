from typing import Optional

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from jsoneditor.forms import JSONEditor

from df_remote_config.models import ConfigAttribute, ConfigPart
from df_remote_config.schema import DEFAULT_SCHEMA


@admin.register(ConfigAttribute)
class ConfigAttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "value")


@admin.register(ConfigPart)
class ConfigPartAdmin(admin.ModelAdmin):
    list_display = ("name", "attributes_", "sequence")

    def get_queryset(self, request: HttpRequest) -> QuerySet[ConfigPart]:
        return super().get_queryset(request).prefetch_related("attributes")

    def attributes_(self, obj: ConfigPart) -> str:
        return "&".join([str(attr) for attr in obj.attributes.all()])

    def get_readonly_fields(
        self, request: HttpRequest, obj: Optional[ConfigPart] = None
    ) -> list[str]:
        if obj:
            return ["name"]
        else:
            return []

    def get_form(self, request, obj=None, **kwargs):  # type: ignore
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields.pop("json", None)
        else:
            form.base_fields["json"].widget = JSONEditor(
                jsonschema=obj.get_schema() or DEFAULT_SCHEMA
            )
        return form
