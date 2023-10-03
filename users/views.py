from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth import authenticate
import jwt
from .utils import (
    get_tokens_for_user, 
    create_activation_token_for_user, 
    set_user_to_active, 
    decode_activation_token,
    send_activation_link,
    get_client_address,
    construct_link,
    )
    

@api_view(['POST'])
def register_user(request):
    """
    Register a new user and sends activation link to user email,  and returns user + token details (user name, token lifetime, etc).
    """
    
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        activation_token, exp_time, token_lifetime_in_mins = create_activation_token_for_user(user)
        
        payload = {
                'user': {
                        'first_name': user.first_name,
                        'email': user.email,
                    },
                'token_details': {
                    'exp_time': exp_time,
                    'token_lifetime_in_mins': token_lifetime_in_mins,
                }
            }

        link = construct_link(
                get_client_address(request), 
                '/activate-account/', 
                activation_token,
            )
        
        mail_server_responded, status_code = send_activation_link(user.first_name, user.email, link)
        
        if mail_server_responded:
            payload['status_code'] = status_code
            payload['message'] = f'Activation mail sent successfully to {user.email}'  
            
            return Response(data=payload, status=status.HTTP_200_OK)
        
        else:
            payload['mail_server']['message'] = f'account registration was successful, but activation link failed to send.'
            return Response({'message': 'cant send email'}, status=status.HTTP_417_EXPECTATION_FAILED)
        
    return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
def activate_account(request):
    """
    Recieves a token as param and activates user account tied to that token.
    """
    
    if request.GET.get('token') is None:
        return Response({'message': 'bad request. no token provided.'}, status=status.HTTP_400_BAD_REQUEST) 
    
    token = request.GET.get('token')
    try:
        payload = decode_activation_token(token)       
    except jwt.DecodeError:
        return Response({'message': 'bad request. token has been tampered with.'}, status=status.HTTP_400_BAD_REQUEST) 
    except jwt.exceptions.ExpiredSignatureError:
        return Response({'message': 'token has expired.'}, status=status.HTTP_403_FORBIDDEN)

    user = set_user_to_active(payload['user_id'])
    return Response({'message': f'account for {user.email} has been activated.'}, status=status.HTTP_200_OK)
   
    
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
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])  
@permission_classes([IsAuthenticated])        
def change_password(request):
    """
    Allows an authenticated user to change their password.
    """
    
    user = request.user
    
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(current_password):
        return Response({'message': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({'message': 'Password has been successfully changed.'}, status=status.HTTP_200_OK)