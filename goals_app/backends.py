import jwt
from jwt.exceptions import PyJWTError

from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from goals_app.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authorization_header_prefix = 'Bearer'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            return None

        prefix = auth_header[0].decode()
        token = auth_header[1]

        if prefix.lower() != self.authorization_header_prefix.lower():
            return None

        return self._authenticate_credentials(token)

    def _authenticate_credentials(self, token):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, settings.JWT_SIGNING_ALGORITHM
            )
        except PyJWTError:
            raise AuthenticationFailed('Could not decode token.')

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

        return user, token
