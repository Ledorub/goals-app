from django.conf import settings
from django.urls import reverse
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from goals_app import models
from goals_app.renderers import UserJSONRenderer
from goals_app import serializers


class RegistrationView(generics.CreateAPIView):
    authentication_classes = []
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    renderer_classes = [UserJSONRenderer]


class LoginView(APIView):
    authentication_classes = []
    serializer_class = serializers.LoginSerializer
    renderer_classes = [UserJSONRenderer]

    def post(self, request):
        data = self.login(data=request.data)
        user = models.User.objects.get(email=data['email'])

        response = Response(data, status=status.HTTP_200_OK)
        add_tokens_to_response(response, user)
        return response

    def login(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.data


class UserRetrieveUpdateView(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    renderer_classes = [UserJSONRenderer]

    def get_object(self):
        return self.request.user


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        return models.Task.objects.filter(parent=None, creator=self.request.user)

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }


class TokenRefreshView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        refresh_token = request.COOKIES.get('refresh_token', None)
        user = request.user

        if not refresh_token:
            pass

        is_token_valid = self.validate_refresh_token(user, refresh_token)
        if not is_token_valid:
            pass

        response = Response(status=status.HTTP_200_OK)
        add_tokens_to_response(response, user)
        return response

    def post(self, request):
        return self.get(request)

    def validate_refresh_token(self, user, value):
        try:
            token = user.refresh_tokens.get(token=value)
        except models.RefreshToken.DoesNotExist:
            raise serializers.ValidationError(
                'Refresh token is not valid.'
            )
        token.invalidate()


def add_tokens_to_response(response, user):
    tokens = user.generate_tokens()

    response.set_cookie(
        key='access_token',
        value=tokens['access_token'],
        max_age=settings.JWT_LIFESPAN / 1000,
        # secure=True,
        httponly=True,
        samesite='strict'
    )
    response.set_cookie(
        key='refresh_token',
        value=tokens['refresh_token'],
        path=reverse('goals-app:refresh-token'),
        # secure=True,
        httponly=True,
        samesite='strict'
    )
    response.headers['X-XSRF-TOKEN'] = tokens['csrf_token']
