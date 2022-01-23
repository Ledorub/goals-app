import jwt
from jwt.exceptions import PyJWTError

from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from goals_app.models import User, CSRFToken


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # If password in data, proceed to username:password authentication.
        if 'password' in request.data:
            return None

        access_token = request.COOKIES.get('access_token', None)
        csrf_token = request.headers.get('X-XSRF-TOKEN', None)

        if not access_token:
            AuthenticationFailed('No token was provided')

        return self._authenticate_credentials(access_token, csrf_token)

    def _authenticate_credentials(self, access_token, csrf_token):
        try:
            payload = decode_access_token(access_token)
        except (ValueError, PyJWTError):
            raise AuthenticationFailed('Provided tokens are invalid.')

        if payload['csrf'] != csrf_token:
            raise AuthenticationFailed(
                'Provided tokens are invalid.'
            )

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise AuthenticationFailed(
                'No account matching this token was found.'
            )

        if not user.is_active:
            raise AuthenticationFailed(
                'Account has been deactivated or has not been activated yet.'
            )

        try:
            user.csrf_tokens.get(token=csrf_token)
        except CSRFToken.DoesNotExist:
            raise AuthenticationFailed(
                'Provided tokens are invalid.'
            )

        return user, access_token


def decode_access_token(token):
    token = token.split()
    if len(token) != 2:
        raise ValueError('Invalid token')

    prefix = token[0]
    if prefix != settings.AUTHORIZATION_TOKEN_PREFIX:
        raise ValueError('Invalid token')

    token = token[1]
    return jwt.decode(
        token, settings.SECRET_KEY, settings.JWT_SIGNING_ALGORITHM
    )
