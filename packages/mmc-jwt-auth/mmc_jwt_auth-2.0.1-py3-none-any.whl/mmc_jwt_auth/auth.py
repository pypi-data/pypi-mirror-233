import jwt, os

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


SIGNING_KEY = os.environ.get('SIGNING_KEY')
AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL')
ACCOUNTS_SERVICE_URL = os.environ.get('ACCOUNTS_SERVICE_URL')

class CustomUser(object):
    def __init__(self, user_data):
        self.__dict__ = user_data
        self.is_authenticated = True
        

class MMCJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the JWT token from the request
        jwt_token = self.get_token_from_request(request)
        
        if jwt_token is None:
            return None  # No token provided
        
        # Make a request to your authentication microservice to validate the token
        user_data = self.validate_token(jwt_token)

        if user_data is None:
            raise AuthenticationFailed('Invalid token')

        # Create a user object based on the user data received from the microservice
        user = CustomUser(user_data)        
        return (user, None)

    def get_token_from_request(self, request):
        # Implement logic to extract the JWT token from the request (e.g., from headers or query parameters)
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None

    def validate_token(self, jwt_token):
        # Decode the JWT token to extract user information (e.g., username)
        try:
            decoded_token = jwt.decode(jwt_token, SIGNING_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token is invalid')

        # Now, you can use the extracted user information (e.g., username) to fetch user data from the accounts service
        email = decoded_token.get('user_data').get('email')
        if email is None:
            raise AuthenticationFailed('Token is invalid. User not found.')

        return decoded_token["user_data"]
