from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import serializers

from goals_app import models


class TokenField(serializers.CharField):
    def __init__(self, **kwargs):
        read_only = kwargs.pop('read_only', True)
        super().__init__(max_length=255, read_only=read_only, **kwargs)

    def __repr__(self):
        return super().__repr__()


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(
            min_length=settings.MIN_PASSWORD_LENGTH,
            max_length=128,
            write_only=True,
            **kwargs
        )


class FieldMixinMetaclass(serializers.SerializerMetaclass):
    def __init__(cls, name, bases, attrs):
        if name.endswith('Mixin'):
            cls.add_get_own_fields_method()

        super().__init__(name, bases, attrs)

    def add_get_own_fields_method(cls):  # TODO: Require fix. Returns all fields for children classes.
        method = classmethod(lambda cls: cls._declared_fields)
        setattr(cls, 'get_own_fields', method)


class AuthFieldsMixin(metaclass=FieldMixinMetaclass):
    username = serializers.CharField(max_length=150)
    password = PasswordField()

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError(
                'An username is required to login.'
            )
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError(
                'A password is required to login.'
            )
        return value


class TokenFieldsMixin(metaclass=FieldMixinMetaclass):
    access_token = TokenField()
    refresh_token = TokenField()


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Counter
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    category = serializers.CharField(max_length=30, source='category.name')
    counter = CounterSerializer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get('user')

    def create(self, validated_data):
        category_name = validated_data.pop('category')['name']
        return models.Task.objects.create(
            creator=self.user,
            category=category_name,
            **validated_data
        )

    def to_representation(self, instance):
        if 'subtasks' not in self.fields:
            self.fields['subtasks'] = TaskSerializer(many=True)
        return super().to_representation(instance)

    class Meta:
        model = models.Task
        fields = ('todo', 'start_date', 'finish_date', 'is_achieved', 'reason',
                  'category', 'counter')


class LoginSerializer(AuthFieldsMixin, TokenFieldsMixin, serializers.Serializer):
    email = serializers.CharField(max_length=254, read_only=True)  # TODO: Remove RO after USERNAME_FIELD change.

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                'A user with corresponding credentials was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This account has been deactivated.'
            )

        return user

    def is_valid(self, raise_exception=True):
        return super().is_valid(raise_exception)

    def to_representation(self, instance):
        return UserWithTokensSerializer(instance).data


class UserWithTokensSerializer(AuthFieldsMixin,
                               TokenFieldsMixin,
                               serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'email', 'username', 'password', 'first_name', 'last_name',
            'access_token', 'refresh_token'
        )


class UserSerializer(UserWithTokensSerializer):
    def __init__(self, *args, **kwargs):
        for field in TokenFieldsMixin.get_own_fields():
            self.fields.pop(field)
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class TokensSerializer(TokenFieldsMixin, serializers.ModelSerializer):
    refresh_token = TokenField(read_only=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get('user', None)

    class Meta:
        model = models.User
        fields = ('access_token', 'refresh_token')

    def create(self, validated_data):
        return self.user

    def validate_refresh_token(self, value):
        try:
            token = self.user.refresh_tokens.get(token=value)
        except models.RefreshToken.DoesNotExist:
            raise serializers.ValidationError(
                'Refresh token is not valid.'
            )
        token.invalidate()
