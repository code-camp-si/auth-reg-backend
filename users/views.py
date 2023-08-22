from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate

@api_view(['POST'])
def register_user(request):
    """
    Register a new user with the given credentials.
    """
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

from django.contrib.auth import get_user_model
@api_view(['POST'])
def login_user(request):
    """
    Authenticates a user with the given credentials, and returns an access token.
    """
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    User = get_user_model()
    user = User.objects.get(username=username)
    
    if user is not None:
        if user.check_password(password):
            # return token here
            return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        # User doesn't exist or credentials are invalid
        return Response({'message': 'User account does not exist.'}, status=status.HTTP_401_UNAUTHORIZED)
