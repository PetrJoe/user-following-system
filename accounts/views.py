from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.decorators import permission_classes
from rest_framework import generics, permissions, status, serializers
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class SignUpView(APIView):

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() # save returns the created user object
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer


class UserDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user