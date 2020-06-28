from django.urls import path, include
from rest_framework.routers import DefaultRouter

from country import views


router = DefaultRouter()
router.register('country', views.CountryViewSet)

app_name = 'country'

urlpatterns = [
    path('', include(router.urls))
]
