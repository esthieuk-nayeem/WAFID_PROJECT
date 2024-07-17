from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.exceptions import ObjectDoesNotExist


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['full_name',  "email", "password"]

    def validate(self, attrs):
        email = attrs.get('email', '')


        # if not phone.isalnum():
        #     raise serializers.ValidationError("The phone should only conatain alphanumeric characters!")

        return attrs

    def create(self, validated_data):
        user_group, created = Group.objects.get_or_create(name='user')
        user = User.objects.create_user(**validated_data)
        user.save()

        user.groups.add(user_group)

        return user




class RegisterAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['full_name', "email", "password"]

    def validate(self, attrs):
        email = attrs.get('phone', '')


        # if not phone.isalnum():
        #     raise serializers.ValidationError("The phone should only conatain alphanumeric characters!")

        return attrs

    def create(self, validated_data):
        admin_group, created = Group.objects.get_or_create(name='admin')
        user = User.objects.create_user(**validated_data)
        user.save()

        user.groups.add(admin_group)

        return user



class LoginSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.IntegerField(read_only=True)
    phone = serializers.CharField(max_length=255, min_length=3,read_only=True)
    full_name = serializers.CharField(max_length=255, min_length=3, read_only=True)
    email = serializers.CharField(max_length=255, min_length=3)
    is_active = serializers.BooleanField(read_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(max_length=255, min_length=3, read_only=True)
    group = serializers.CharField(max_length=255, read_only=True)


    class Meta:
        model = User
        fields = ["id", "phone","email", "is_active", "password", 'token', 'full_name', 'group', 'username']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        try:
            _user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise AuthenticationFailed("Email does not exist!")

        user = auth.authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid Credentials!")

        if not user:
            raise AuthenticationFailed("Invalid Credentials!")

        if not user.is_active:
            raise AuthenticationFailed("Account Disabled, Contact Admin!")

        token = Token.objects.get(user=_user)
        group = Group.objects.filter(user=user)
        print(group[0].name)
        print(token)

        return {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'is_active': user.is_active,
            'token': token.key,
            'group': group[0].name,

        }


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'is_varified']  # Include the 'phone' and 'is_varified' fields for updating


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad token")