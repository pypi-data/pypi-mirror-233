from django.db import models
from django.utils.module_loading import import_string
from model_utils.models import TimeStampedModel

from df_remote_config.fields import NoMigrationsChoicesField
from df_remote_config.schema import DEFAULT_SCHEMA, PART_SCHEMAS
from df_remote_config.settings import api_settings


class ConfigAttribute(models.Model):  # type: ignore
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}={self.value}"

    class Meta:
        unique_together = ("name", "value")


class ConfigPartQuerySet(models.QuerySet):
    def filter_attributes(self, attributes: dict[str, str]) -> "ConfigPartQuerySet":
        if not attributes:
            return self

        attribute_condition = models.Q()
        for name, value in attributes.items():
            attribute_condition |= models.Q(name=name, value=value)
        return self.filter(
            attributes__in=ConfigAttribute.objects.filter(attribute_condition)
        )


class ConfigPart(TimeStampedModel):
    objects = ConfigPartQuerySet.as_manager()
    name = NoMigrationsChoicesField(
        max_length=255, choices=[(part, part) for part in api_settings.PARTS]
    )
    sequence = models.PositiveIntegerField(default=1000)
    attributes = models.ManyToManyField(ConfigAttribute, blank=True)
    json = models.JSONField(blank=True, default=dict)

    def __str__(self) -> str:
        return f"ConfigPart<{self.id}>: {self.name}"

    def get_schema(self) -> dict:
        # If the schema is not defined in the settings, use the default schema
        if "SCHEMA" not in api_settings.PARTS[self.name]:
            return PART_SCHEMAS.get(self.name, DEFAULT_SCHEMA)

        return import_string(api_settings.PARTS[self.name]["SCHEMA"])

    class Meta:
        ordering = ("sequence",)
