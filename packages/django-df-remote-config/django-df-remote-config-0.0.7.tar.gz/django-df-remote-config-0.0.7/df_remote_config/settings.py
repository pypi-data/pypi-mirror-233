from typing import Any

from django.conf import settings
from rest_framework.settings import APISettings

DEFAULTS: dict[str, Any] = {
    "PARTS": {
        "legal": {
            "HANDLER_CLASS": "df_remote_config.handlers.DefaultHandler",
        },
        "default": {},
        "app_launch": {
            "HANDLER_CLASS": "df_remote_config.handlers.AppLaunchHandler",
        },
    },
    "DEFAULT_PART": "default",
}

api_settings = APISettings(getattr(settings, "DF_REMOTE_CONFIG", None), DEFAULTS)
