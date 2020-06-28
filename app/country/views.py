from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Country

from country import serializers


class CountryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    '''Manage countries in the database'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        '''Returns objects for the current authenticated user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''Create a new country'''
        serializer.save(user=self.request.user)
