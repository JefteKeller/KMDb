from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from .serializers import AccountSerializer, LoginSerializer


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            username=request.data['username'],
            password=request.data['password'],
        )
        if not user:
            return Response(
                {'detail': 'Unable to log in with provided credentials.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})
