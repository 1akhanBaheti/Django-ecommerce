from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User
from ..serializers.auth_serializers import SignUpSerializer,SignInSerializer
from store.models import Profile
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.db import transaction
from django.shortcuts import get_object_or_404

class sign_up(APIView):
    def post(self,request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            Profile.objects
            user =User(**serializer.validated_data)
            user.set_password(serializer.validated_data['password'])
            user.save()
            Profile.objects.create(user_id=user.id)

        return Response("OK")

class sign_in(APIView):
    def post(self,request):
        signInSerializer = SignInSerializer(data=request.data)
        signInSerializer.is_valid(raise_exception=True)
        user=authenticate(request=request, email= signInSerializer.validated_data['email'],password= signInSerializer.validated_data['password'])
        if user is None:
            raise ValidationError({
                "error" : "USER NOT EXISTS"
            })
        else:
            profile = get_object_or_404(Profile,user_id=user.id)
            refresh = RefreshToken.for_user(user=user)
            data ={
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                **model_to_dict(user),
                **model_to_dict(profile),
            }
        return Response(data)