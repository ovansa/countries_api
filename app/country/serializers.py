from rest_framework import serializers

from core.models import Country, State


class CountrySerializer(serializers.ModelSerializer):
    '''Serializer for countries objects'''

    class Meta:
        model = Country
        fields = ('id', 'name')
        read_only_fields = ('id',)


class StateSerializer(serializers.ModelSerializer):
    '''Serializer for state objects'''

    class Meta:
        model = State
        fields = ('id', 'name')
        read_only_fields = ('id',)
