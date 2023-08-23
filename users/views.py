from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from .utils import get_tokens_for_user


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

    
@api_view(['POST'])
def login_user(request):
    """
    Authenticates a user with the given credentials, and returns an access token.
    """
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token = get_tokens_for_user(user)
        
        return Response({'message': 'Auth Successful.', 'token': token}, status=status.HTTP_200_OK)
    else:
        # User doesn't exist or credentials are invalid
        return Response({'message': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])        
def user_profile(request):
    """
    Returns user profile if user is authenticated.
    """
    
    serializer = UserSerializer(request.user)
    return Response({'user_profile': serializer.data}, status=status.HTTP_200_OK)
    