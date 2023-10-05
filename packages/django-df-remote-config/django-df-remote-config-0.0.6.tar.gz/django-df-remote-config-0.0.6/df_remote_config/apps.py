from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DfRemoteConfigConfig(AppConfig):
    name = "df_remote_config"
    verbose_name = _("Django DF Remote Config")

    class DFMeta:
        api_path = "remoteconfig/"
