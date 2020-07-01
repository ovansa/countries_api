from rest_framework import serializers

from core.models import Country, State, Place


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


class PlaceSerializer(serializers.ModelSerializer):
    '''Serializer for a place'''
    country = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Country.objects.all()
    )

    state = serializers.PrimaryKeyRelatedField(
        many=True, queryset=State.objects.all()
    )

    class Meta:
        model = Place
        fields = ('id', 'name', 'country', 'state')
        read_only_fields = ('id',)


class PlaceDetailSerializer(PlaceSerializer):
    '''Serialize a place detail'''
    state = StateSerializer(many=True, read_only=True)
    country = CountrySerializer(many=True, read_only=True)
