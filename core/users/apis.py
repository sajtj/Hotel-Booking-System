from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from core.users.models import BaseUser , Profile
from core.common.mixins import ApiAuthMixin
from core.users.selectors import get_profile
from core.users.services import register 
from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_validator, letter_validator

from drf_spectacular.utils import extend_schema


class RegisterApi(APIView):

    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(
            validators = [
                MinLengthValidator(limit_value=10),
                number_validator,
                special_char_validator,
                letter_validator
            ]
        )
        confirm_password = serializers.CharField(max_length=255)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists() :
                raise serializers.ValidationError("Email Already Taken.")
            return email
        
        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data


    class OutputRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("email", "created_at", "updated_at")


    @extend_schema(request=InputRegisterSerializer, responses=OutputRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try :
            user = register(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password")
                )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutputRegisterSerializer(user, context={'request':request}).data)
    
    

class ProfileApi(ApiAuthMixin, APIView):

    class OutPutSerializer(serializers.ModelSerializer):
        user = serializers.EmailField(source="user.email")

        class Meta:
            model = Profile 
            fields = ("user",)


    @extend_schema(responses=OutPutSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(self.OutPutSerializer(query, context={"request":request}).data)