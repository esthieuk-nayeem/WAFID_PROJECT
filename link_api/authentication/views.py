from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .models import User
from rest_framework.views import APIView
from rest_framework import generics, status, permissions


# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        print(user)
        serializer.save()

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)




class RegisterAdminView(generics.GenericAPIView):
    serializer_class = RegisterAdminSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user_instance = serializer.save()

        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)



class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class UserVarifyView(APIView):
    def put(self, request):
        phone_number = request.data.get('phone')  # Assuming the phone number is provided in the request data

        try:
            user = User.objects.get(phone=phone_number)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update the is_varified attribute for the found user
        user.is_varified = True  # Update the attribute based on your condition
        user.save()

        serializer = UserUpdateSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)