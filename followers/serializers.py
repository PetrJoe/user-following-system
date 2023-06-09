from rest_framework import serializers
from .models import Follower
from django.conf import settings
from django.contrib.auth import get_user_model


User = settings.AUTH_USER_MODEL
User = get_user_model()

class FollowerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follower
        fields = ['id', 'user', 'follower']

    def validate_follower(self, value):
        user = self.context['request'].user
        if value == user:
            raise serializers.ValidationError("You cannot follow yourself.")
        if Follower.objects.filter(user=user, follower=value).exists():
            raise serializers.ValidationError("You are already following this user.")
        return value



class MyFollowerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.CharField(source='follower.username')
    email = serializers.EmailField(source='follower.email')

    class Meta:
        model = Follower
        fields = ['id', 'user', 'follower', 'username', 'email']