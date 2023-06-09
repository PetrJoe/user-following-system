from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()




class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to validate and create a new user
    """
    class Meta:
        model = User
        fields = ['id','email', 'password','username', 'first_name', 'last_name','middle_name', 'gender']
        extra_kwargs = {'password': {'write_only': True}}



class SignUpSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    email = serializers.EmailField(required=True)    

    class Meta:
        model = User
        fields = ['id','username','first_name','middle_name','last_name','email','password', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            gender=validated_data['gender'],
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    refresh = RefreshToken.for_user(user)
                    return {
                        'email': user.email,
                        'token': str(refresh.access_token),
                        # 'refresh_token': str(refresh)
                    }
                else:
                    raise serializers.ValidationError('User is not active')
            else:
                raise serializers.ValidationError('Incorrect email or password')
        else:
            raise serializers.ValidationError('Email and password are required')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance