from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.conf import settings
from .models import Follower
from .serializers import *

User = settings.AUTH_USER_MODEL


@api_view(['POST'])
# @csrf_exempt
@permission_classes([IsAuthenticated])
def follow_user(request):
    data = request.data.copy()
    data['user'] = request.user.pk
    serializer = FollowerSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'message': 'User followed successfully'})
    return Response(serializer.errors, status=400)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_follower(request, follower_id):
    # get the authenticated user
    user = request.user    
    try:
        # get the follower object
        follower = Follower.objects.get(id=follower_id, user=user)
        follower.delete()
        return Response({"status": "success", "message": "Successfully Unfollow User"}, status=status.HTTP_204_NO_CONTENT)
    except Follower.DoesNotExist:
        return Response({"error": "Follower not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_followers(request):
    # Retrieve the authenticated user's followers
    followers = Follower.objects.filter(user=request.user)
    # Serialize the followers and return the response with status 200 - OK
    serializer = MyFollowerSerializer(followers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
