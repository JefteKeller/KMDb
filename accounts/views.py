from rest_framework.generics import CreateAPIView

from django.contrib.auth.models import User
from .serializers import AccountSerializer


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
