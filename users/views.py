from rest_framework import permissions, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import RegisterSerializer
from .address_serializers import AddressSerializer
from .models import Address
from .tasks import send_welcome_email


class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        send_welcome_email.delay(user.email)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class AddressViewSet(viewsets.ModelViewSet):

    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
