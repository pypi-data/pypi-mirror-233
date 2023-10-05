from rest_framework import serializers


class RemoteConfigSerializer(serializers.Serializer):
    part = serializers.DictField()
