from rest_framework import serializers
from ..models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =Profile
        fields= ['phone','birth_date']


class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, allow_null=True)
    birth_date = serializers.DateField(allow_null=True)

    
    