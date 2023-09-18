from rest_framework_simplejwt.tokens import RefreshToken
from core import settings
from datetime import datetime, timedelta
import jwt
from django.contrib.auth.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
def create_activation_token_for_user(user):
    exp_time = datetime.utcnow() + settings.SIMPLE_JWT.get('ACTIVATION_TOKEN_LIFETIME')
    token = jwt.encode(
            {'user_id': user.id, 'exp': exp_time}, 
            settings.SECRET_KEY, 
            algorithm='HS256',
        )
    token_lifetime_in_mins = settings.SIMPLE_JWT.get('ACTIVATION_TOKEN_LIFETIME').total_seconds() / 60
    return token, exp_time, token_lifetime_in_mins



def decode_activation_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    return payload
           

def set_user_to_active(id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return user