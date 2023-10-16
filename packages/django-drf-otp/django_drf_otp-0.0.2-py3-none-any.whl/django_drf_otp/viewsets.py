from typing import Dict, Type

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .enums import NotificationType
from .serializers import OTPTokenSerializer, OTPTokenVerifySerializer
from .services import OTPService
from .settings import otp_settings


class OTPTokenViewSet(GenericViewSet):
    permission_classes = (AllowAny,)
    service = OTPService()
    LOGIN = "login"
    VERIFY_TOKEN = "verify_token"
    serializer_classes = {
        LOGIN: OTPTokenSerializer,
        VERIFY_TOKEN: OTPTokenVerifySerializer,
    }

    def login(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if otp_settings.ENABLE_OTP_AUTHENTICATION:
            extra_context = self.get_extra_context_data(request=request, validated_data=serializer.validated_data)
            self.service.generate_and_notify_token(user=serializer.validated_data["user"], extra_context=extra_context)

        data = self.get_success_response_data(validated_data=serializer.validated_data, **kwargs)
        return Response(data=data, status=status.HTTP_200_OK)

    def verify_token(self, request: Request, *args, **kwargs):
        if not otp_settings.ENABLE_OTP_AUTHENTICATION:
            return Response(data={"message": _("Otp authentication is disabled.")}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = self.get_success_response_data(validated_data=serializer.validated_data, **kwargs)
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self, *args, **kwargs) -> Type[serializers.Serializer]:
        return self.serializer_classes[self.action]

    def get_success_response_data(self, validated_data: Dict, **kwargs) -> Dict:
        if self.action == self.LOGIN and otp_settings.ENABLE_OTP_AUTHENTICATION:
            return {"message": _("OTP token sent successfully.")}
        else:
            token, created = Token.objects.get_or_create(user=validated_data["user"])
            return {"token": token.key}

    def get_extra_context_data(self, request: Request, validated_data: Dict) -> Dict:
        context = {"request": request}

        user = validated_data["user"]
        default_notification_type = otp_settings.DEFAULT_NOTIFICATION_TYPE

        nofification_type = (
            user.notification_preference.notification_type
            if hasattr(user, "notification_preference")
            else default_notification_type
        )
        if nofification_type == NotificationType.EMAIL:
            context.update(
                {"first_name": user.first_name, "last_name": user.last_name, "full_name": user.get_full_name()}
            )

        return context
