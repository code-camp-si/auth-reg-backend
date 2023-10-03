from rest_framework_simplejwt.tokens import RefreshToken
from core import settings
from datetime import datetime
import jwt
from django.contrib.auth.models import User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_activation_link(name: str, email: str, link: str) -> bool:
    """
    Sends an activation link to the provided email. Returns True if mail was successfully sent.
    """

    subject = 'Auth-Reg Activate your Account: Link Activation'
    message = f'Hi {name},\nclick on this link to activate your account: \n\n{link}'

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email,
        subject=subject,
        plain_text_content=message,
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return True, response.status_code
    except Exception as e:
        return False, str(e)

  
def get_client_address(request):
    """
    Returns the base uri of where request is made from.
    """
    
    return f'{request.scheme}://{request.get_host()}' 


def construct_link(address, path, param):
    """
    Constructs a url link from a base address, a path, and params.
    note: incomplete, sufficient for only one param. In future, param should be a dict.
    """
    
    return f'{address}{path}?token={param}'
   
    
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