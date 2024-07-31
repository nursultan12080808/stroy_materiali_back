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
     path('user/<int:id>', UserViewSet.as_view()),

    path('auth/login/', LoginApiView.as_view()),
    path('auth/register/', RegisterApiView.as_view()),
    
    path('redactor_profile/<int:id>/', RedactorProfileApiView.as_view()),

    path('', include(router.urls)),
]