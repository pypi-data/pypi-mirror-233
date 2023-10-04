from rest_framework import serializers


class RemoteConfigSerializer(serializers.Serializer):
    data = serializers.JSONField()
