from rest_framework import serializers


class TruckDataSerializer(serializers.Serializer):
    coordinate_x = serializers.IntegerField(required=True, min_value=0)
    coordinate_y = serializers.IntegerField(required=True, min_value=0)


class StorageDataSerializer(serializers.Serializer):
    trucks_data = serializers.DictField(child=TruckDataSerializer())


class ValidateFormSerializer(serializers.Serializer):
    storage_data = serializers.DictField(child=StorageDataSerializer())
