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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Token
        fields = '__all__'

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


class UserViewSet(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)
    

class TokenViewSet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticatedOrReadOnly, IsSalesmanOrReadOnly, IsOwnerProductOrReadOnly)



class LoginApiView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token': token.key
            })
        return Response({'detail': 'Не существуеет пользователя либо неверный пароль.'}, status.HTTP_400_BAD_REQUEST)


class RedactorProfileApiView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = request.data.get('password')
        if(password):
            if check_password(password, user.password):
                new_password = request.data.get('password1')
                user.set_password(new_password)
                user.save()
            else:
                return Response({'error': 'Пароль неверный'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key
        })
    


class RegisterApiView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key
        })