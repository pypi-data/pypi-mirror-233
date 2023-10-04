import json
from typing import Optional

from django.db.models import Max
from django.http import HttpRequest
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from df_remote_config.models import ConfigPart


class AbstractHandler:
    def handle_request(self, request: HttpRequest, part_name: str) -> Response:
        raise NotImplementedError


class DefaultHandler(AbstractHandler):
    def get_config_part(
        self, request: HttpRequest, part_name: str
    ) -> Optional[ConfigPart]:
        attributes = json.loads(request.GET.get("attributes", "{}"))

        return (
            ConfigPart.objects.filter(name=part_name)
            .filter_attributes(attributes)
            .first()
        )

    def get_part_data(self, part: ConfigPart) -> dict:
        return part.json

    def handle_request(self, request: HttpRequest, part_name: str) -> Response:
        if config_part := self.get_config_part(request, part_name):
            return Response({"data": self.get_part_data(config_part)})
        else:
            raise NotFound()


class AppLaunchHandler(DefaultHandler):
    def get_part_data(self, part: ConfigPart) -> dict:
        data = super().get_part_data(part)

        data["updates"] = {
            "parts": {
                part["name"]: part["modified"].isoformat()
                for part in ConfigPart.objects.values("name").annotate(
                    modified=Max("modified")
                )
            }
        }

        return data
