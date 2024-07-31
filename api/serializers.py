from django.db import transaction
from rest_framework import serializers
from stroy.models import *
from django.contrib.auth.password_validation import validate_password
from drf_extra_fields.fields import Base64ImageField
from account.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')



class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tags
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"


class CompaniesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"



class MaterialSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=Base64ImageField(), required=False)   
    class Meta:
        model = Material
        fields = "__all__"

    def update(self, instance, validated_data):
        images = validated_data.pop('images', [])
        material = super().update(instance, validated_data)
        for image in images:
            image_name = image.name
            image_file = image

            material_image = Images.objects.create(material=material)
            material_image.image.save(image_name, image_file)
        return material
    

class MaterialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'
    


class ListMaterialSerializer(serializers.ModelSerializer):
    images = MaterialImageSerializer(many=True)
    tags = TagSerializer(many=True)
    company = CompaniesSerializer()
    user = UserSerializer()

    class Meta:
        model = Material
        exclude = ('description',)



class DetailMaterialSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = MaterialImageSerializer(many=True)
    tags = TagSerializer(many=True)
    company = CompaniesSerializer()

    class Meta:
        model = Material
        fields = '__all__'




class CreateMaterialSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=Base64ImageField(), required=False)   

    class Meta:
        model = Material
        fields = '__all__'

    @transaction.atomic()
    def create(self, validated_data):
        images = validated_data.pop('images', [])
        material = super().create(validated_data)

        
        for image in images:
            image_name = image.name
            image_file = image

            material_image = Images.objects.create(material=material)
            material_image.image.save(image_name, image_file)

        return material
    


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions')


class RegisterSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()  # Используем Base64ImageField вместо ListSerializer
    password1 = serializers.CharField(validators=[validate_password])
    password2 = serializers.CharField()

    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'password', 'is_superuser', 'groups', 'user_permissions',)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        
        if password1 != password2:
            raise serializers.ValidationError({
                'password2': ['Пароли не совпадают!']
            })

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        validated_data['password'] = make_password(password)

        return super().create(validated_data)