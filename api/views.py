from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsOwnerProductOrReadOnly, IsSalesmanOrReadOnly, IsAdminUserOrReadOnly, IsSalesman
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from api.paginations import MediumPagination
from .filters import MaterialFilter
from django.core.mail import send_mail
from .serializers import *
from account.models import User

class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    lookup_field = 'id'
    serializer_class = {
        'list': ListMaterialSerializer,
        'retrieve': DetailMaterialSerializer,
        'create': CreateMaterialSerializer,
        'update': MaterialSerializer,
    }
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MaterialFilter
    pagination_class = MediumPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerProductOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return self.serializer_class['update']
        return self.serializer_class[self.action] 
    


class CategporyViewSet(ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'id'
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerProductOrReadOnly)



class TagsViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    lookup_field = 'id'
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerProductOrReadOnly)



class CompaniesViewSet(ModelViewSet):
    queryset = Company.objects.all()
    lookup_field = 'id'
    serializer_class = CompaniesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerProductOrReadOnly)