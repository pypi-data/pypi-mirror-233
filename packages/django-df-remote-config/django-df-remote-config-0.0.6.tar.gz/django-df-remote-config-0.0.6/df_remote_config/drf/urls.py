from django.urls import path

from .views import RemoteConfigView

urlpatterns = [path("", RemoteConfigView.as_view(), name="remote-config")]
