from rest_framework import serializers

from core.models import Country


class CountrySerializer(serializers.ModelSerializer):
    '''Serializer for countries objects'''

    class Meta:
        model = Country
        fields = {'id', 'name'}
        read_only_fields = {'id', }
