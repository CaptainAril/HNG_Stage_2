from django.contrib.auth.hashers import make_password
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        Serializer)

from .models import Organisation, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'userId',
            'firstName',
            'lastName',
            'email',
            'phone'
        ]


class OrganisationSerializer(ModelSerializer):
    class Meta:
        model = Organisation
        fields = [
            'orgId',
            'name',
            'description'
        ]
    
    def create(self, validated_data):
        org = Organisation.objects.create(owner=self.context.get('request').user, **validated_data)
        return org
    


class LoginSerializer(Serializer):
    email = EmailField(required=True)
    password = CharField(required=True)


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'firstName',
            'lastName',
            'email',
            'password',
            'phone'
        ]

    def create(self, validated_data):
        validated_data['password'] =  make_password(password=validated_data.get('password'))
        user = User.objects.create(**validated_data)
    
        return user
        # return super(RegisterUserSerializer, self).create(validated_data)
