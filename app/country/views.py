from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Country, State

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
