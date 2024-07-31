from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('materials', MaterialViewSet)
router.register('categories', CategporyViewSet)
router.register('tags', TagsViewSet)
router.register('companies', CompaniesViewSet)


urlpatterns = [
    path('', include(router.urls)),
]