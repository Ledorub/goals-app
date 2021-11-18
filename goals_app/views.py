from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from goals_app import models
from goals_app.renderers import UserJSONRenderer
from goals_app import serializers


class RegistrationView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserWithTokensSerializer
    renderer_classes = [UserJSONRenderer]


class LoginView(APIView):
    serializer_class = serializers.LoginSerializer
    renderer_classes = [UserJSONRenderer]

    def post(self, request):
        data = self.login(data=request.data)
        return Response(data, status=status.HTTP_200_OK)

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


class TokenRefreshView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TokensSerializer
    renderer_classes = [UserJSONRenderer]

    def get_serializer_context(self):
        return {
            'user': self.request.user
        }
