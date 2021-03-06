from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Country, State, Place

from country import serializers


# Re-factor country and state viewsets to BaseCountryAttrViewset
class BaseCountryAttrViewset(viewsets.GenericViewSet, mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    '''Base viewset for user owned country attributes'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''Returns objects for the current authenticated user'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''Create a new object'''
        serializer.save(user=self.request.user)


class CountryViewSet(BaseCountryAttrViewset):
    '''Manage countries in the database'''
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer


class StateViewSet(BaseCountryAttrViewset):
    '''Manage states in the database'''
    queryset = State.objects.all()
    serializer_class = serializers.StateSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    '''Manage places in database'''
    serializer_class = serializers.PlaceSerializer
    queryset = Place.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''Retrieve places for authenticated user'''
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        '''Return appropriate serializer class'''
        if self.action == 'retrieve':
            return serializers.PlaceDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        '''Create a new place'''
        serializer.save(user=self.request.user)
