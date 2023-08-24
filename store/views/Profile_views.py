from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.viewsets import GenericViewSet
from ..serializers.profile_serializers import ProfileSerializer,UserProfileSerializer
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models import Profile
from core.serializers.user_serializers import UserSerializer
from rest_framework.response import Response
from django.db import transaction
from django.forms.models import model_to_dict

class ProfileView(APIView):

    def get(self,request):
        try:
            profile =Profile.objects.select_related('user').get(user_id=request.user.id)
            return Response(ProfileSerializer(profile).data)
        except Profile.DoesNotExist:
            return Response({'detail':'Not Found'},status=404)
    
    def patch(self,request):
        try:
            with transaction.atomic():
                
                profile =Profile.objects.select_related('user').get(user_id=request.user.id)
                userSerializer =UserSerializer(request.user,data=request.data,partial=True)
                userSerializer.is_valid(raise_exception=True)
                request.user=userSerializer.save()
                profileSerializer =ProfileSerializer(profile,data=request.data,partial=True)
                profileSerializer.is_valid(raise_exception=True)
                profile= profileSerializer.save()
                data ={
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    **model_to_dict(profile),
                }
                userProfile = UserProfileSerializer(data=data)
                userProfile.is_valid(raise_exception=True)
                return Response(userProfile.data)
        except Profile.DoesNotExist:
            return Response({'detail':'Not Found'},status=404)



    
